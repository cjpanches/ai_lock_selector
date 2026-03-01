# AR Measurement Technology

## Overview

AR (Augmented Reality) технология используется для визуального наложения эталонного контура euro cylinder на изображение замка для помощи пользователю в позиционировании камеры и калибровки измерений.

## Euro Cylinder Dimensions (CRITICAL REFERENCE)

**Source of Truth**: `mask/euro_profile_exact.svg`

```
┌─────────────────────┐
│    ┌─────────┐      │  ← Top circle: 17mm diameter (r=8.5mm)
│    │         │      │
│    │ 10mm    │      │  ← Slot width: 10mm (CALIBRATION REFERENCE!)
│    │         │      │
│    └─────────┘      │
│        ────          │
│      ╱      ╲        │  ← Bottom: 10mm diameter (r=5mm)
│    ╱        ╲       │
└─────────────────────┘

Total height: 33mm
```

### Key Dimensions

| Parameter | Value | Usage |
|-----------|-------|-------|
| Total Height | 33mm | Full cylinder height |
| Top Circle Diameter | 17mm | Top circular part |
| Slot Width | **10mm** | **CALIBRATION REFERENCE** |
| Bottom Diameter | 10mm | Bottom semicircle |

## Calibration Formula

```python
# CRITICAL: Scale calibration using euro cylinder
pixels_per_mm = detected_slot_width_pixels / 10.0
```

**Why 10mm?**
- The slot width of euro cylinder is a fixed, standardized dimension
- It's visible in almost every lock photo
- It provides reliable scale reference

## AR Overlay

### Mask File
- **Location**: `mask/euro_profile_exact.svg`
- **Format**: SVG (scalable)
- **Usage**: AR overlay in Flutter app

### Rendering
1. Load `euro_profile_exact.svg`
2. Convert to Flutter widget (CustomPaint or SvgPicture)
3. Overlay on camera preview
4. Allow user to position camera until cylinder aligns

## Measurement Process

### Step 1: Object Detection (YOLO)
Detect 3 classes:
- `lock_plate` - entire visible lock plate
- `cylinder_hole` - euro cylinder hole (33x17mm silhouette)
- `handle_square` - handle square hole (8x8mm)

### Step 2: Scale Calculation
```python
# From cylinder_hole bounding box
bbox_width = x2 - x1
bbox_height = y2 - y1

# Slot is the narrower dimension (10mm reference)
slot_width_px = min(bbox_width, bbox_height)
scale_factor = slot_width_px / 10.0  # pixels per mm
```

### Step 3: Measurements
```python
# Using scale_factor
backset = distance(cylinder_center, handle_center) / scale_factor
center_distance = backset  # Same in this project
plate_width = plate_bbox_width / scale_factor
plate_height = plate_bbox_height / scale_factor
```

## Measurement Tolerances

| Parameter | Tolerance | Range |
|-----------|-----------|-------|
| Backset | ±2mm | 20-68mm |
| Center Distance | ±3mm | 50-92mm |
| Plate Width | ±2mm | 3-8mm |
| Plate Height | ±3mm | 150-280mm |

## Validation

### Scale Factor Validation
```python
MIN_SCALE_FACTOR = 5.0   # px/mm
MAX_SCALE_FACTOR = 50.0  # px/mm
```

### Aspect Ratio Validation
```python
# Euro cylinder aspect ratio: 33/10 = 3.3
VALID_ASPECT_RATIO_RANGE = (1.5, 4.0)
```

## Important Notes

1. **Never use mounting_holes for center distance** - They measure cylinder→handle distance, not cylinder→mounting
2. **Always use cylinder_hole for scale** - 10mm slot is the calibration reference
3. **Handle square center is the measurement point** - Not the hole edge, but center

## Related Documents

- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Calibration details
- [mask/euro_profile_exact.svg](./mask/euro_profile_exact.svg) - Source of truth
- [06_CV_MODEL_SPEC.md](./06_CV_MODEL_SPEC.md) - CV specification
