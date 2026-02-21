# AI Lock Selector

Мобильное приложение для точного измерения параметров дверных замков через AR и подбора аналогов из каталога компании.

## Описание

Приложение использует дополненную реальность для калибровки масштаба по стандартному отверстию цилиндра DIN, затем компьютерное зрение вычисляет размеры замка, а алгоритм подбирает аналоги из базы данных.

## Возможности

- AR-маска DIN для точной калибровки масштаба
- Измерение: backset, межосевое расстояние, размеры планки, корпуса
- Подбор аналогов с fuzzy matching (±2-3 мм)
- Каталог замков компании

## Структура проекта

```
ai_lock_project/
├── mobile_app/          # Flutter приложение
├── backend/             # FastAPI сервер
├── cv_pipeline/         # Компьютерное зрение (Python)
└── docs/                # Документация
```

## Быстрый старт

### Требования
- Flutter 3.24+
- Python 3.10+
- JDK 17

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile App
```bash
cd mobile_app
flutter pub get
flutter run
```

### Сборка APK
```bash
cd mobile_app
flutter build apk --debug
```

## API Endpoints

- `POST /api/v1/measure` - Измерение параметров замка
- `POST /api/v1/match` - Подбор аналогов
- `GET /api/v1/locks` - Список замков

## Технологии

- Flutter + Riverpod
- FastAPI + PostgreSQL
- OpenCV + YOLO
- ARCore / ARKit

## Лицензия

MIT
