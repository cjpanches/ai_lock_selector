# AI Lock Selector - Продолжение разработки

## Текущее состояние

**Ветка:** develop  
**GitHub:** https://github.com/cjpanches/ai_lock_selector

## О проекте

Мобильное приложение для измерения параметров дверных замков через AR и подбора аналогов.

## Структура

```
ai_lock_project/
├── mobile_app/          # Flutter приложение
│   ├── lib/
│   │   ├── core/constants.dart
│   │   ├── domain/models/
│   │   │   ├── capture_context.dart
│   │   │   └── lock_profile.dart
│   │   ├── features/
│   │   │   ├── ar_camera/ar_camera_screen.dart
│   │   │   └── measurement/measurement_result_screen.dart
│   │   └── main.dart
│   └── pubspec.yaml
│
├── backend/             # FastAPI
│   ├── app/
│   │   ├── api/       # endpoints
│   │   ├── services/  # business logic
│   │   └── models/    # schemas
│   └── requirements.txt
│
└── cv_pipeline/        # Computer Vision
    └── src/
        ├── contour_analyzer.py
        ├── edge_detector.py
        └── geometry_calculator.py
```

## Что нужно сделать

### Приоритет 1: CV Pipeline
Реализовать реальный контурный анализ в `cv_pipeline/src/`:
- Поиск контура планки замка
- Детекция крепёжных отверстий
- Детекция квадрата ручки
- Расчёт размеров в мм

### Приоритет 2: YOLO Модель
- Обучить или использовать готовую модель для детекции замков
- Сегментация контуров

### Приоритет 3: База данных
- Подключить PostgreSQL
- Создать таблицы: locks, manufacturers, compatibility
- Парсить чертежи с сайта компании

### Приоритет 4: UI
- Улучшить визуальную маску DIN
- Анимация совмещения
- Экран каталога замков

## Ключевые константы

```dart
// Mobile
const double dinCylinderWidth = 10.0;   // мм
const double dinCylinderHeight = 17.0;  // мм
const double backsetTolerance = 2.0;
const double centerDistanceTolerance = 3.0;
```

## Команды

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Flutter
cd mobile_app && flutter run

# APK
cd mobile_app && flutter build apk --debug
```

## Работа с Git

- Ветка `master` защищена, только через Pull Request
- Работать в `develop`
- Коммиты в `develop`, затем создать PR в `master`

## Документация

- `AGENTS.md` - инструкции для AI
- `CONTRIBUTING.md` - руководство для разработчиков
- `docs/` - техническая документация

---

Начни с изучения текущего кода в `cv_pipeline/src/` и улучши контурный анализ для реального распознавания замков.
