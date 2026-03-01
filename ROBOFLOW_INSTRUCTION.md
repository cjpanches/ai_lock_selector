# ROBOFLOW INSTRUCTION FOR AI LOCK SELECTOR
# ===========================================
# Project: AI Lock Selector - врезные дверные замки
# Target: YOLOv8 Oriented Bounding Box
# Date: 2026-02-28
# ===========================================

## 1. PROJECT OVERVIEW

**Goal:** Detect and measure врезные (врезные) дверные замки from photo
**Target Accuracy:** ±0.5mm - ±1.0mm
**Method:** AR marker (DIN) for scale calibration + YOLO detection + OpenCV measurement

## 2. WHAT TO DETECT - 4 MAIN CLASSES

### Class 0: lock_plate (Планка замка)
**Description:** Металлическая планка (лицевая пластина) замка
**Visual:** Большой прямоугольный контур, обрамляющий весь замок
**Typical sizes:**
- Width (толщина планки): 3-8mm
- Height (высота планки): 150-280mm
- Материал: сталь, цвет: серебро/золото/хром/бронза

**How to label:** Draw rectangle around entire visible lock plate (наружная металлическая планка)

---

### Class 1: cylinder_hole (Отверстие под цилиндр / Euro cylinder)
**Description:** Отверстие для установки цилиндрового механизма (евроцилиндр)
**Visual:** Сложная форма - верхняя часть полукруглая (⌀17mm), затем вертикальный слот шириной 10mm, затем нижняя полуокружность (⌀10mm)
**Total size: 33mm height x 17mm width**

**Exact geometry (from engineering drawing):**
- Total height: **33mm**
- Top circle: diameter **17mm** (radius 8.5mm)
- Vertical slot: width **10mm** (x=11.5mm to x=21.5mm)
- Bottom semicircle: radius **5mm** (diameter 10mm)
- The **10mm slot** is the "bridge" connecting the two circles

**How to label:** Draw polygon/OBB around the entire Euro cylinder hole silhouette (the entire 33x17mm shape)

---

### Class 2: handle_square (Квадрат ручки)
**Description:** Квадратное отверстие для установки дверной ручки
**Visual:** Квадратное отверстие, обычно в средней/нижней части замка
**Standard sizes:**
- 8x8mm (most common)
- 9x9mm
- 10x10mm

**How to label:** Draw rectangle around square hole

---

## 3. OPTIONAL CLASSES (if visible)

### Class 4: din_marker (DIN reference - if using separate marker)
**Description:** Специальный DIN маркер (если используется отдельный референс)
**Size:** 33mm x 17mm (same as cylinder_hole geometry)
**Note:** Usually the cylinder_hole (class 1) IS the DIN marker - no need for separate class

---

## 4. MEASUREMENT REFERENCE - KEY SIZES

### From Database (147 locks):
| Parameter | Min | Max | Typical |
|-----------|-----|-----|---------|
| Backset (мм) | 20 | 68 | 45-55 |
| Center Distance (мм) | 50 | 92 | 70-85 |
| Plate Height (мм) | 150 | 280 | 200-235 |
| Plate Width (толщина, мм) | 3 | 8 | 5-7 |
| Square Size (мм) | 8 | 10 | 8 |

### Critical Measurements for Matching:
1. **Backset (Бэксет):** Расстояние от центра цилиндра до центра квадрата ручки
2. **Center Distance (Межосевое):** Расстояние от центра цилиндра до центра ручки (или до крепёжных отверстий)
3. **Plate Dimensions:** Габариты планки замка

---

## 5. TOLERANCES FOR MATCHING

| Parameter | Tolerance | Priority |
|-----------|-----------|----------|
| Backset | ±2.0mm | HIGH |
| Center Distance | ±3.0mm | HIGH |
| Plate Width | ±2.0mm | MEDIUM |
| Plate Height | ±3.0mm | MEDIUM |

---

## 6. PHOTO REQUIREMENTS

### Optimal Conditions:
- **Angle:** Strictly top-down (сверху, перпендикулярно двери)
- **Lighting:** Good, even lighting (избегать теней)
- **Focus:** Sharp, no blur
- **Background:** Clean, contrasting
- **Scale:** DIN marker (10x17mm hole) must be clearly visible

### Photo Format:
- Resolution: minimum 640x640 (prefer 1280x720+)
- Format: JPG or PNG
- Color: Color or grayscale both OK

### What MUST be visible:
1. Entire lock plate
2. Cylinder hole (for scale reference!)
3. Handle square hole

---

## 7. ANNOTATION FORMAT

### YOLOv8 OBB Format (Oriented Bounding Box):
```
<class_id> <cx> <cy> <w> <h> <angle>
```

Where:
- class_id: 0-3 (or 0-4)
- cx, cy: center coordinates (normalized 0-1)
- w, h: width, height (normalized 0-1)
- angle: rotation in radians (0 for axis-aligned)

### Or use Roboflow Polygon format:
Draw polygons around each object - Roboflow will convert automatically.

---

## 8. RECOMMENDED DATASET STRUCTURE

```
project/
├── train/
│   ├── image_001.jpg
│   ├── image_001.txt (labels)
│   └── ...
├── valid/
│   ├── image_101.jpg
│   ├── image_101.txt
│   └── ...
└── data.yaml
```

### Minimum dataset size:
- Training: 500+ images
- Validation: 50-100 images (10-20%)

---

## 9. TRAINING RECOMMENDATIONS

### YOLOv8 Settings:
```bash
# Model: yolov8n-obb.pt (nano - fastest) or yolov8s-obb.pt (small - better)
model: yolov8n-obb.pt

# Training
epochs: 100
imgsz: 640
batch: 16
patience: 10

# Augmentation
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 5.0
translate: 0.1
scale: 0.5
fliplr: 0.5
```

### Expected metrics:
- mAP50: >0.7 for good detection
- mAP50-95: >0.5

---

## 10. SCALE CALIBRATION (CRITICAL!)

### How Calibration Works:
The **cylinder_hole (class 1)** serves as the SCALE REFERENCE for ALL measurements in the application.

### Formula:
```python
# Using the 10mm SLOT WIDTH (vertical bridge between circles)
pixels_per_mm = detected_slot_width_pixels / 10.0
```

### Why 10mm?
- The 10mm is the **slot width** (the vertical "bridge" between top circle and bottom semicircle)
- This is the most reliable vertical dimension in the Euro cylinder shape
- It stays consistent across different cylinder brands

### Using for Measurements:
```python
# After detecting objects with YOLO:
backset_mm = distance_pixels / pixels_per_mm
plate_width_mm = width_pixels / pixels_per_mm
# etc.
```

### Important:
- Always label the **entire** cylinder_hole silhouette (the full 33x17mm shape)
- The YOLO model will detect the full shape
- The application will calculate scale using the 10mm slot width
- This provides accuracy of ±0.5-1.0mm

---

## 11. HOW TO USE IN APPLICATION

### Flow:
1. User takes photo with AR mask (DIN marker visible)
2. YOLO detects lock components
3. OpenCV measures distances using scale from DIN hole
4. Results matched against database

### Example Output:
```json
{
  "backset_mm": 45.2,
  "center_distance_mm": 72.0,
  "plate_width_mm": 5.5,
  "plate_height_mm": 235.0,
  "confidence": 0.89,
  "detected_classes": {
    "lock_plate": [x, y, w, h],
    "cylinder_hole": [x, y, w, h],
    "handle_square": [x, y, w, h]
  }
}
```

---

## 11. FILES IN PROJECT

| File | Path | Description |
|------|------|-------------|
| Training script | cv_pipeline/train_yolo.py | YOLO training |
| Pre-labeling | cv_pipeline/pre_label.py | Auto-generate labels |
| Dataset config | cv_pipeline/dataset/lock_dataset.yaml | Dataset config |
| CV Pipeline | cv_pipeline/src/geometry_calculator.py | Measurement logic |
| Database | backend/locks.db | 147 locks with dimensions |

---

## 12. REFERENCES

- GitHub: https://github.com/cjpanches/ai_lock_selector
- Branch: develop
- Roboflow: https://roboflow.com/

---

**IMPORTANT:** The cylinder_hole (class 1) is the MOST critical class - it serves as the SCALE REFERENCE for all measurements. Always label it accurately!
