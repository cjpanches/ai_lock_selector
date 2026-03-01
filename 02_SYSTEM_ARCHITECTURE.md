# System Architecture

## Overview

AI Lock Selector - мобильное приложение для измерения параметров дверных замков по фотографии с использованием AR калибровки и подбора аналогов из базы данных.

## Components

### 1. Backend (FastAPI)
- **Port**: 8001
- **Database**: SQLite (147 замков)
- **API**: RESTful endpoints для работы с замками
- **Location**: `backend/`

**Tech Stack:**
- FastAPI
- SQLAlchemy (async)
- Pydantic
- Uvicorn

### 2. Flutter Mobile App
- **Platforms**: Android, iOS, Web
- **State Management**: Riverpod
- **Router**: GoRouter
- **Location**: `mobile_app/`

**Tech Stack:**
- Flutter 3.41
- Dart 3.11
- Riverpod
- GoRouter

### 3. CV Pipeline (Python)
- **Purpose**: Обработка изображений, детекция объектов, измерения
- **ML Model**: YOLOv8 OBB
- **Location**: `cv_pipeline/`

**Tech Stack:**
- Python 3.12
- OpenCV
- Ultralytics (YOLO)
- NumPy

### 4. Database
- **Current**: SQLite (`backend/locks.db`)
- **Tables**: locks, manufacturers, lock_compatibility, measurements
- **Records**: 147 замков

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐
│   Flutter App  │────▶│   Backend API   │
│  (Mobile/Web)  │     │   (FastAPI)     │
└────────┬────────┘     └────────┬────────┘
         │                      │
         │              ┌────────▼────────┐
         │              │    SQLite DB    │
         │              │  (147 locks)    │
         │              └─────────────────┘
         │
         ▼
┌─────────────────┐
│  CV Pipeline    │
│  (YOLO + OpenCV)│
└─────────────────┘
```

## Data Flow

1. **User** фотографирует замок через Flutter приложение
2. **Flutter** отправляет изображение на Backend API
3. **CV Pipeline** обрабатывает изображение:
   - YOLO детектирует объекты (lock_plate, cylinder_hole, handle_square)
   - Вычисляется scale_factor по цилиндру (10mm slot)
   - Измеряются: backset, center_distance, plate dimensions
4. **Matching Service** ищет аналоги в базе данных
5. **Flutter** отображает результаты с AR маской

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/locks` | GET | Список замков |
| `/api/v1/locks/{id}` | GET | Получить замок |
| `/api/v1/measure` | POST | Измерить по фото |
| `/api/v1/match` | POST | Подобрать аналоги |
| `/api/v1/cv/process` | POST | Обработать изображение |

## Key Configuration

- **Euro Cylinder Dimensions**: 33mm height, 10mm slot width (calibration reference)
- **Scale Factor Formula**: `pixels_per_mm = detected_slot_width_pixels / 10.0`
- **Measurement Tolerances**:
  - Backset: ±2mm
  - Center Distance: ±3mm
  - Plate Width: ±2mm

## Environment Variables

```
DATABASE_URL=sqlite+aiosqlite:///./locks.db
PYTHONPATH=.
FLUTTER_WEB_PORT=8083
BACKEND_PORT=8001
```

## Related Documents

- [01_REQUIREMENTS.md](./01_REQUIREMENTS.md) - Требования
- [03_AI_PIPELINE.md](./03_AI_PIPELINE.md) - AI/ML конвейер
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Быстрый старт
