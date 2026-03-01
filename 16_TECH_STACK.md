# Tech Stack

## Overview

Технологический стек проекта AI Lock Selector.

## Frontend

### Mobile App

| Technology | Version | Purpose |
|------------|---------|---------|
| Flutter | 3.41.2 | Cross-platform framework |
| Dart | 3.11.0 | Programming language |
| Riverpod | ^2.5.0 | State management |
| GoRouter | ^14.0.0 | Navigation |
| camera | ^0.11.0 | Camera access |
| flutter_svg | ^2.0.10 | SVG rendering |

### Web Build

| Technology | Purpose |
|------------|---------|
| Flutter Web | Web deployment |
| HTML/CSS/JS | Compiled output |

## Backend

### Core

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Programming language |
| FastAPI | ^0.110.0 | Web framework |
| Uvicorn | ^0.27.0 | ASGI server |
| Pydantic | ^2.6.0 | Data validation |
| SQLAlchemy | ^2.0.0 | ORM |

### Database

| Technology | Purpose |
|------------|---------|
| SQLite (current) | Development database |
| PostgreSQL (planned) | Production database |
| aiosqlite | Async SQLite driver |
| asyncpg | Async PostgreSQL driver |

### Testing

| Technology | Purpose |
|------------|---------|
| pytest | Test framework |
| httpx | HTTP client for tests |
| pytest-asyncio | Async test support |

## CV/ML

### Computer Vision

| Technology | Purpose |
|------------|---------|
| OpenCV | Image processing |
| NumPy | Numerical computing |
| Ultralytics | YOLO framework |

### Model

| Component | Value |
|-----------|-------|
| Framework | YOLOv8 |
| Mode | OBB (Oriented Bounding Box) |
| Model Size | nano (yolov8n-obb.pt) |
| Classes | 3 (lock_plate, cylinder_hole, handle_square) |

## Infrastructure

### Development

| Tool | Purpose |
|------|---------|
| Git | Version control |
| GitHub | Remote repository |
| VS Code | IDE |
| Python LSP | Language server |

### Deployment (Planned)

| Component | Technology |
|-----------|------------|
| Backend | Docker + Kubernetes |
| Database | PostgreSQL |
| Hosting | Cloud provider |

## Project Structure

```
ai_lock_project/
├── mobile_app/           # Flutter app
│   ├── lib/
│   │   ├── features/     # Screens
│   │   ├── providers/    # Riverpod providers
│   │   ├── models/       # Data models
│   │   └── core/         # Router, constants
│   ├── test/
│   └── build/            # Compiled web
│
├── backend/              # FastAPI app
│   ├── app/
│   │   ├── api/         # Routes
│   │   ├── db/          # Models & DB
│   │   ├── services/    # Business logic
│   │   └── core/        # Config
│   ├── tests/
│   └── locks.db         # SQLite DB
│
├── cv_pipeline/          # CV pipeline
│   ├── src/
│   │   ├── lock_pipeline.py
│   │   ├── yolo_detector.py
│   │   ├── geometry_calculator.py
│   │   └── contour_analyzer.py
│   ├── dataset/
│   └── train_yolo.py
│
├── mask/                # AR masks
│   └── euro_profile_exact.svg
│
└── datafordb/           # Training images
```

## Dependencies

### Backend (requirements.txt)
```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
pydantic>=2.6.0
pydantic-settings>=2.1.0
pytest>=7.4.0
httpx>=0.27.0
aiosqlite>=0.19.0
```

### CV Pipeline
```
opencv-python>=4.9.0
numpy>=1.26.0
ultralytics>=8.1.0
```

### Mobile App (pubspec.yaml)
```yaml
dependencies:
  flutter_riverpod: ^2.5.0
  go_router: ^14.0.0
  camera: ^0.11.0
  flutter_svg: ^2.0.10
  http: ^1.2.0
```

## Environment Variables

```bash
# Backend
DATABASE_URL=sqlite+aiosqlite:///./locks.db
PYTHONPATH=.
DEBUG=true

# Flutter
API_BASE_URL=http://127.0.0.1:8001

# CV Pipeline
MODEL_PATH=runs/obb/train/weights/best.pt
CONFIDENCE_THRESHOLD=0.5
```

## Related Documents

- [AGENTS.md](./AGENTS.md) - Implementation details
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Quick start
- [README.md](./README.md) - Project overview
