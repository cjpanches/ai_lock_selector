# Руководство для AI-агентов

## Общее описание проекта

Проект AI Lock Selector - это мобильное приложение для измерения параметров дверных замков с использованием AR и компьютерного зрения. Основная идея - использовать стандартное отверстие цилиндра DIN как эталон масштаба.

## Архитектура

```
mobile_app/           # Flutter (Dart)
  lib/
    core/            # Константы, конфиг
    domain/models/   # Сущности (LockProfile, LockModel, CaptureContext)
    features/
      ar_camera/    # AR экран с маской DIN
      measurement/  # Логика измерений
      matching/     # Алгоритм подбора
    data/           # API клиент, CV компоненты

backend/              # FastAPI (Python)
  app/
    api/             # Endpoints
    services/        # Business logic
    models/          # Pydantic схемы
    db/              # Database

cv_pipeline/          # Computer Vision
  src/
    contour_analyzer.py
    edge_detector.py
    geometry_calculator.py
```

## Ключевые модели данных

### LockProfile (Dart)
```dart
class LockProfile {
  LockDimensions dimensions;  // backset, centerDistance, plateWidth, etc.
  List<MountingHole> mountingHoles;
  HandleSquarePosition? handleSquare;
  CylinderHolePosition? cylinderHole;
  double confidence;
  DateTime capturedAt;
}
```

### LockDimensions
```dart
class LockDimensions {
  double backset;        // расстояние от края до центра цилиндра (мм)
  double centerDistance; // межосевое расстояние (мм)
  double plateWidth;     // ширина планки (мм)
  double plateHeight;    // высота планки (мм)
  double bodyWidth;      // ширина корпуса (мм)
  double bodyHeight;     // высота корпуса (мм)
}
```

## Алгоритм измерения

1. **Калибровка**: Пользователь совмещает маску DIN с отверстием цилиндра
2. **Масштаб**: scale = pixels / 10mm (ширина узкой части DIN)
3. **CV**: Контурный анализ для поиска планки, отверстий, ручки
4. **Расчёт**: Все размеры умножаются на scale

## Алгоритм подбора (Matching)

```python
# tolerance (мм)
TOLERANCES = {
    "backset": 2.0,
    "center_distance": 3.0,
    "plate_width": 2.0,
    "plate_height": 3.0,
}

# веса параметров
WEIGHTS = {
    "backset": 0.35,
    "center_distance": 0.30,
    "plate_width": 0.15,
    "plate_height": 0.10,
}
```

## Типичные задачи

### Добавить новый параметр измерения
1. Добавить поле в LockDimensions (Dart и Python)
2. Обновить CV пайплайн для расчёта
3. Обновить UI для отображения

### Улучшить точность CV
1. Работать в cv_pipeline/src/
2. Использовать OpenCV функции
3. Тестировать на реальных фото

### Добавить новый API эндпоинт
1. Создать в backend/app/api/
2. Добавить pydantic схему в models/
3. Подключить service логику

## Важные константы

```dart
// Mobile
const double dinCylinderWidth = 10.0;   // мм
const double dinCylinderHeight = 17.0;  // мм
const double backsetTolerance = 2.0;    // мм
const double centerDistanceTolerance = 3.0; // мм
```

## Тестирование

```bash
# Flutter
cd mobile_app
flutter test

# Backend
cd backend
pytest
```

## Сборка

```bash
# APK
cd mobile_app
flutter build apk --debug

# Backend (Docker)
cd backend
docker build -t ai-lock-backend .
```

---

## Подсистема анализа AI-экспертов (Subsystem1)

Структура для мульти-экспертного анализа проекта с использованием AI систем.

### Структура директорий

```
subsystem1/
├── subsystem1.py           # Main orchestrator
├── INFO/                    # Входные данные и результаты
│   ├── Grok/               # Эксперт Grok (xAI)
│   ├── Gemini/             # Эксперт Gemini (Google)
│   ├── GPT/                # Эксперт GPT (OpenAI)
│   ├── Copilot/            # Эксперт Copilot (GitHub)
│   ├── Analysis/           # Комбинированный анализ
│   └── GENERAL PLAN/       # Супер-промты для AI
├── FACT/                   # Фактический текущий анализ
├── IDEAL PLAN/             # Идеальный план развития
└── logs/                   # Логи (игнорятся в git)
```

### Использование Grok эксперта

```bash
# Запуск анализа
cd subsystem1
python subsystem1.py

# Установка API ключа Grok (опционально)
export GROK_API_KEY="your-api-key"
```

### Добавление нового эксперта

1. Создать директорию `INFO/{ExpertName}/`
2. Добавить класс эксперта в `subsystem1.py`
3. Обновить `Subsystem1Orchestrator`

### Логирование

Все действия логируются в:
```
subsystem1/logs/action_{YYYYMMDD}.log
```

### Тесты

```bash
cd subsystem1
pytest test_subsystem1.py -v
```
