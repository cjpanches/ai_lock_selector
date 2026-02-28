# AI LOCK SELECTOR - COMPLETE PROJECT DOCUMENTATION
# ====================================================
# For AI/ML Engineers and Developers
# Version: 4.3.0
# Date: 2026-02-28
# ====================================================

## 1. PROJECT PURPOSE

**AI Lock Selector** - мобильное приложение для Android/iOS, которое позволяет:
1. Сфотографировать врезной дверной замок
2. Автоматически определить тип замка по фото
3. Измерить ключевые размеры с точностью ±0.5-1.0mm
4. Подобрать аналоги из базы данных

---

## 2. TARGET HARDWARE

- **Platform:** Android (Flutter)
- **Camera:** Minimum 8MP with autofocus
- **Display:** 720p+ recommended
- **Target user:** Мастера по установке замков, продавцы замков

---

## 3. WHAT LOCKS WE DETECT

### Lock Types:
- **Врезные замки** (mortise locks) - основной тип
- Euro profile cylinders (евроцилиндр)

### Brands in Database:
- Apecs (Россия)
- Avers (Россия)

---

## 4. CRITICAL MEASUREMENTS

### Primary (used for matching):

| Measurement | Russian | Description | Range (mm) | Tolerance |
|-------------|---------|-------------|------------|-----------|
| Backset | Бэксет | Center of cylinder to center of handle square | 20-68 | ±2.0mm |
| Center Distance | Межосевое | Cylinder center to handle center (or mounting holes) | 50-92 | ±3.0mm |

### Secondary (for verification):

| Measurement | Russian | Description | Range (mm) |
|-------------|---------|-------------|------------|
| Plate Width | Ширина планки | Thickness of lock plate | 3-8 |
| Plate Height | Высота планки | Height of visible lock plate | 150-280 |
| Square Size | Размер квадрата | Handle square hole (usually 8x8) | 8-10 |
| Mounting Hole | Крепёжное отверстие | Diameter of mounting holes | 6-12 |

---

## 5. CALIBRATION METHOD

### DIN Marker (Critical!)
The **cylinder hole** serves as the scale reference:
- Euro cylinder total size: **33mm height x 17mm width**
- Top circle: diameter **17mm**
- **Slot width: 10mm** (the vertical "bridge" between circles)
- Bottom semicircle: diameter **10mm**

Formula: `scale_factor = slot_width_pixels / 10.0`

**Note:** The 10mm slot is the most reliable dimension for calibration.

---

## 6. TECHNICAL STACK

### Frontend (Mobile App)
- **Framework:** Flutter 3.41.2
- **State Management:** Riverpod 2.x
- **Navigation:** GoRouter
- **Camera:** camera package
- **Architecture:** Clean Architecture (features/providers/core)

### Backend
- **Framework:** FastAPI
- **Database:** SQLite (aiosqlite) → PostgreSQL (future)
- **ORM:** SQLAlchemy 2.0 (async)
- **Validation:** Pydantic v2
- **Port:** 8001

### CV Pipeline
- **Detection:** YOLOv8 (OBB - Oriented Bounding Box)
- **Image Processing:** OpenCV 4.x
- **Python:** 3.x
- **Scripts:** 
  - `train_yolo.py` - Training
  - `pre_label.py` - Auto-labeling

---

## 7. DATABASE SCHEMA

### Table: locks (147 records)
```sql
locks (
    id INTEGER PRIMARY KEY,
    vendor_code VARCHAR(50),
    name VARCHAR(255),
    brand VARCHAR(100),
    type VARCHAR(10),          -- ' врезной'
    backset FLOAT NOT NULL,    -- Бэксет (мм)
    center_distance FLOAT,     -- Межосевое (мм)
    plate_width FLOAT,         -- Ширина планки (мм)
    plate_height FLOAT,        -- Высота планки (мм)
    square_hole_size FLOAT,   -- Размер квадрата (мм)
    lock_cylinder_hole VARCHAR(20)  -- напр "33x17"
)
```

### Table: measurements (for storing results)
```sql
measurements (
    id INTEGER PRIMARY KEY,
    lock_id INTEGER,
    backset_measured FLOAT,
    center_distance_measured FLOAT,
    plate_width_measured FLOAT,
    plate_height_measured FLOAT,
    confidence FLOAT,
    image_path VARCHAR(500)
)
```

---

## 8. API ENDPOINTS

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/locks | GET | List all locks |
| /api/v1/locks/{id} | GET | Get lock by ID |
| /api/v1/match | POST | Find matching locks by measurements |
| /api/v1/measure | POST | Process image and measure |
| /health | GET | Health check |

### Match Request Example:
```json
POST /api/v1/match
{
  "backset": 45.0,
  "center_distance": 72.0,
  "tolerance_backset": 2.0,
  "tolerance_center": 3.0
}
```

---

## 9. CV PIPELINE FLOW

```
Input Image (with AR mask)
         ↓
    ┌─────────────┐
    │ Preprocess  │ → grayscale, blur, edge detection
    └─────────────┘
         ↓
    ┌─────────────┐
    │ YOLO Detect │ → find lock_plate, cylinder_hole, 
    │             │   mounting_hole, handle_square
    └─────────────┘
         ↓
    ┌─────────────┐
    │ Calculate   │ → use DIN hole (10mm) for scale
    │ Scale       │ → pixels_per_mm = hole_width / 10
    └─────────────┘
         ↓
    ┌─────────────┐
    │ Measure     │ → backset, center_distance,
    │ Dimensions  │   plate dimensions
    └─────────────┘
         ↓
    ┌─────────────┐
    │ Match DB    │ → find closest locks
    └─────────────┘
         ↓
    Output: JSON with measurements + matched locks
```

---

## 10. YOLO CLASSES (4-5 classes)

| Class ID | Name | Description | Detection Priority |
|----------|------|-------------|-------------------|
| 0 | lock_plate | Вся планка замка | HIGH |
| 1 | cylinder_hole | Отверстие цилиндра (10x17mm) | CRITICAL |
| 2 | mounting_hole | Крепёжные отверстия (2 шт) | HIGH |
| 3 | handle_square | Квадрат ручки (8x8mm) | HIGH |
| 4 | din_marker | DIN маркер (если отдельный) | LOW |

**NOTE:** class 1 (cylinder_hole) is CRITICAL - it's the scale reference!

---

## 11. FILES REFERENCE

### Core Files:
| File | Purpose |
|------|---------|
| `cv_pipeline/train_yolo.py` | Train YOLO model |
| `cv_pipeline/pre_label.py` | Auto-generate labels from CV |
| `cv_pipeline/src/geometry_calculator.py` | Calculate measurements |
| `cv_pipeline/src/contour_analyzer.py` | Find contours |
| `cv_pipeline/dataset/lock_dataset.yaml` | Dataset config |
| `backend/app/main.py` | FastAPI app |
| `backend/app/api/v1/locks.py` | Lock endpoints |
| `backend/app/api/v1/match.py` | Matching logic |
| `mobile_app/lib/features/ar_camera/` | AR camera screen |
| `mobile_app/lib/features/catalog/` | Lock catalog |

### Documentation:
| File | Purpose |
|------|---------|
| `PROJECT_STATE.md` | Current project state |
| `ROBOFLOW_INSTRUCTION.md` | Labeling guide for Roboflow |
| `AI_EXPERTS/` | Expert analysis results |
| `STARTUP.md` | How to start development |

---

## 12. STARTUP COMMANDS

### Backend:
```bash
cd backend
uvicorn app.main:app --port 8001 --reload
```

### Mobile App:
```bash
cd mobile_app
flutter run
```

### Train YOLO:
```bash
cd cv_pipeline
python train_yolo.py --epochs 100
```

---

## 13. CURRENT STATUS (v4.3)

| Component | Status | Notes |
|----------|--------|-------|
| Backend | ✅ Working | 147 locks in DB |
| Mobile App | ✅ Working | AR camera + catalog |
| CV Pipeline | ⚠️ Ready | Needs trained YOLO |
| YOLO Dataset | ❌ In Progress | Collecting photos |
| Tests | ✅ 38 tests | Backend unit tests |

---

## 14. REPOSITORY

- **GitHub:** https://github.com/cjpanches/ai_lock_selector
- **Branch:** develop
- **License:** MIT

---

## 15. KEY CONSTANTS (from code)

```python
# geometry_calculator.py
DIN_CYLINDER_WIDTH = 10.0   # mm
DIN_CYLINDER_HEIGHT = 17.0 # mm
BACKSET_TOLERANCE = 2.0    # mm
CENTER_DISTANCE_TOLERANCE = 3.0  # mm

# Standard lock measurements
TYPICAL_SQUARE_SIZES = [8, 9, 10]  # mm
TYPICAL_BACKSETS = [25, 30, 35, 40, 45, 50, 55, 60, 65, 68]  # mm
TYPICAL_CENTER_DISTANCES = [50, 55, 60, 65, 70, 72, 75, 80, 85, 90, 92]  # mm
```

---

**This document is for AI/ML engineers to understand:**
1. What the lock looks like
2. What measurements matter
3. How calibration works (DIN hole = scale reference)
4. What YOLO should detect

**Key insight:** The cylinder_hole (class 1) is both an object to detect AND the calibration reference. Label it accurately!
