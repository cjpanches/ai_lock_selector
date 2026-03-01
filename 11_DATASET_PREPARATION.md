# Dataset Preparation

## Overview

Подготовка датасета для обучения YOLO модели детекции замков.

## Data Sources

### Primary Source
- **Location**: `datafordb/`
- **Count**: 762 images
- **Format**: JPG
- **Content**: Photos of various door locks

### Data Characteristics

| Property | Value |
|----------|-------|
| Total Images | 762 |
| Format | JPG, PNG |
| Resolution | Varies (typically 800x600 to 1920x1080) |
| Color | Color and grayscale |
| Quality | Mixed (some annotated, some raw) |

## Dataset Structure

```
datafordb/
├── 2/
│   ├── Замки врезные. Apecs_files/
│   │   ├── 20395_annotated.jpg
│   │   ├── 16946_annotated.jpg
│   │   └── ...
│   └── 3/
│       └── Замок врезной Apecs 2210_60-B_G_files/
├── Торговая компания АПЕКС СЕКЬЮРИТИ_files/
│   ├── 02a1bbb5018d1ab8281de8ee27bbc053.jpg
│   └── ...
└── ... (other directories)
```

## Preparation Steps

### Step 1: Image Collection
- Photos already collected in `datafordb/`
- Additional photos can be added to this folder
- Supported formats: JPG, PNG

### Step 2: Quality Filtering
- Remove duplicate images
- Remove low-quality images (blurry, dark)
- Keep images with visible lock plate, cylinder, and handle

### Step 3: Roboflow Upload
```bash
# Option 1: Manual upload via Roboflow UI
# 1. Go to roboflow.com
# 2. Create new project
# 3. Upload images

# Option 2: Use Roboflow API
pip install roboflow
roboflow upload datafordb/ -p lock-detection
```

### Step 4: Labeling (3 Classes)

| Class ID | Name | Description | Label Guideline |
|----------|------|-------------|-----------------|
| 0 | lock_plate | Entire visible lock plate | Draw polygon around plate |
| 1 | cylinder_hole | Euro cylinder hole | Draw around ENTIRE 33x17mm silhouette |
| 2 | handle_square | Handle square hole | Draw rectangle around 8x8mm square |

### Step 5: Dataset Split
Recommended split:
- Training: 70% (533 images)
- Validation: 20% (152 images)
- Test: 10% (77 images)

### Step 6: Export
- Format: YOLOv8 OBB (Oriented Bounding Boxes)
- Download and place in `cv_pipeline/dataset/`

## Current Dataset Config

```yaml
# cv_pipeline/dataset/lock_dataset.yaml
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

## Pre-labeling Script

Для помощи в разметке можно использовать скрипт:
```bash
cd cv_pipeline
python pre_label.py --input ../datafordb --output dataset/
```

Это создаст предварительные labels на основе CV анализа.

## Data Augmentation

Roboflow supports automatic augmentation:
- Flip (horizontal, vertical)
- Rotation (±15°)
- Brightness/Contrast
- Blur
- Noise

Recommended: Enable all augmentations for better model generalization.

## Quality Metrics

| Metric | Target |
|--------|--------|
| Images | 500+ |
| Annotations per image | 1-4 |
| Class balance | ~equal |
| mAP50 (after training) | >0.8 |

## Related Documents

- [ROBOFLOW_INSTRUCTION.md](./ROBOFLOW_INSTRUCTION.md) - Detailed labeling guide
- [cv_pipeline/train_yolo.py](./cv_pipeline/train_yolo.py) - Training script
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Quick start
