# AGENTS.md - Инструкции для AI агентов

## О проекте

AI Lock Selector - приложение для измерения дверных замков по фото с AR калибровкой.

## Текущее состояние

- ✅ Flutter app с AR экраном
- ✅ Backend API (FastAPI)
- ✅ CV Pipeline (заготовка)
- ✅ Debug APK собран

## Что нужно доработать

### 1. CV Pipeline (ПРИОРИТЕТ)
```
cv_pipeline/src/
- contour_analyzer.py - сейчас stub
- edge_detector.py - сейчас stub
- geometry_calculator.py - сейчас stub
```

Задача: Реализовать реальный контурный анализ с использованием OpenCV для нахождения:
- Контура планки замка
- Крепёжных отверстий
- Квадрата ручки
- Отверстия цилиндра

### 2. YOLO Модель
Обучить или использовать готовую модель для:
- Детекции замка на фото
- Сегментации контуров
- Классификации типа замка

### 3. База данных
Заменить in-memory данные на PostgreSQL:
- Таблица locks
- Таблица manufacturers
- Таблица compatibility
- Парсинг чертежей с сайта компании

### 4. UI/UX
- Улучшить визуальную маску DIN
- Добавить анимацию совмещения
- Улучшить экран результатов

## Технические детали

### Масштаб
Ключевая формула:
```python
scale_factor = marker_width_pixels / 10.0  # 10mm = ширина слота в евроцилиндре
```

### Точность
- Цель: ±1.5 мм
- Используем: DIN отверстие как эталон

### Matching
```python
# Fuzzy tolerance
backset: ±2mm
center_distance: ±3mm
plate_width: ±2mm
plate_height: ±3mm
```

## Работа с кодом

### Flutter
- State management: Riverpod
- UI: Material 3
- Камера: camera package

### Backend
- Framework: FastAPI
- DB: SQLAlchemy + asyncpg
- Validation: Pydantic

### CV
- OpenCV 4.x
- YOLOv8
- NumPy

## Команды

```bash
# Запуск backend
cd backend && uvicorn app.main:app --reload

# Flutter run
cd mobile_app && flutter run

# Build APK
cd mobile_app && flutter build apk --debug
```

## Конвенции

### Dart
- Использовать Equatable для моделей
- camelCase для переменных
- flutter_riverpod для state

### Python
- pydantic для моделей
- async/await для I/O
- OpenCV для CV

## Контакты

Для вопросов по архитектуре - см. docs/01_REQUIREMENTS.md
