# CV Model Specification

## Overview

Computer Vision pipeline использует YOLOv8 для детекции объектов и OpenCV для геометрических измерений.

## YOLO Model

### Model Configuration
- **Framework**: Ultralytics YOLOv8
- **Mode**: OBB (Oriented Bounding Boxes)
- **Model**: yolov8n-obb.pt (nano - fastest)
- **Training**: Not yet trained (needs Roboflow)

### Classes (3)

| ID | Class | Description | Label |
|----|-------|-------------|-------|
| 0 | lock_plate | Металлическая планка замка | Draw around entire visible lock plate |
| 1 | cylinder_hole | Euro cylinder hole (33x17mm) | Draw around ENTIRE silhouette (not just slot!) |
| 2 | handle_square | Квадрат ручки (8x8mm) | Draw rectangle around square hole |

### Why These Classes?

1. **lock_plate** - Identifies the lock, provides plate dimensions
2. **cylinder_hole** - CRITICAL: Provides BOTH object detection AND scale calibration
3. **handle_square** - Provides measurement point for backset/center_distance

**Note**: mounting_hole was removed (not needed for center distance measurement)

## Dataset

### Location
- **Photos**: 762 images in `datafordb/`
- **Dataset config**: `cv_pipeline/dataset/lock_dataset.yaml`

### Format
```yaml
path: ./dataset
train: images/train
val: images/val
test: images/test

nc: 3
names:
  0: lock_plate
  1: cylinder_hole
  2: handle_square

obb: true
```

## CV Pipeline Components

### 1. YOLODetector (`yolo_detector.py`)
```python
CLASSES = {
    0: "lock_plate",
    1: "cylinder_hole",
    2: "handle_square",
}
```

### 2. ContourAnalyzer (`contour_analyzer.py`)
- Finds geometric shapes
- Identifies holes, rectangles
- Filters by expected dimensions

### 3. EdgeDetector (`edge_detector.py`)
- Canny edge detection
- Morphological operations
- ROI extraction

### 4. LockPipeline (`lock_pipeline.py`)
- Main orchestration
- Scale factor calculation
- Feature extraction

### 5. GeometryCalculator (`geometry_calculator.py`)
- Distance calculations
- Dimension conversions
- Coordinate transformations

## Scale Factor Calculation

```python
def calculate_scale_factor(marker_bbox):
    """
    marker_bbox: (x, y, w, h) from YOLO
    
    CRITICAL: Use min dimension for slot width (10mm)
    """
    w, h = marker_bbox[2], marker_bbox[3]
    slot_width_px = min(w, h)
    
    # Euro cylinder slot = 10mm
    scale_factor = slot_width_px / 10.0
    
    # Validation
    assert 5.0 <= scale_factor <= 50.0
    
    return scale_factor
```

## Measurements

### From YOLO Detections
```python
# For each detection
bbox = detection.bbox  # (x, y, w, h)
width_mm = bbox[2] / scale_factor
height_mm = bbox[3] / scale_factor
```

### Center Distance (Backset)
```python
# Distance between cylinder center and handle center
center_distance = calculate_distance(
    cylinder_hole_center,
    handle_square_center
) / scale_factor
```

## Accuracy Target

| Measurement | Target Accuracy |
|-------------|-----------------|
| Backset | ±0.5-1.0mm |
| Center Distance | ±0.5-1.0mm |
| Plate Width | ±1.0mm |
| Plate Height | ±2.0mm |

## Training

### Command
```bash
cd cv_pipeline
python train_yolo.py --epochs 100
```

### Expected Output
- Model weights: `runs/obb/train/weights/best.pt`
- Metrics: precision, recall, mAP50-95

## Related Documents

- [ROBOFLOW_INSTRUCTION.md](./ROBOFLOW_INSTRUCTION.md) - Labeling guide
- [cv_pipeline/train_yolo.py](./cv_pipeline/train_yolo.py) - Training script
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Quick start
