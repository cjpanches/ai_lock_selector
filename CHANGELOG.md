# Журнал разработки

## v4.4.0 - YOLO & Documentation Update (01.03.2026)

### Исправления
- Критический баг: scale_factor теперь использует min(w,h) вместо max(w,h)
- Добавлена валидация aspect ratio (1.5-4.0)
- Добавлена валидация scale factor (5-50 px/mm)

### Изменения YOLO классов
- Удалён класс mounting_hole (не нужен для center distance)
- Теперь 3 класса: lock_plate, cylinder_hole, handle_square
- Обновлены конфиги: lock_dataset.yaml, classes.txt

### Документация
- Заполнены все 13 пустых placeholder файлов (02-17 серия)
- Добавлен LICENSE (MIT)
- Добавлены GitHub templates: issue, PR
- Обновлены все ссылки на классы

### Очистка
- Удалён subsystem1/ (legacy)
- Удалены одноразовые файлы: info.txt, idealist.txt, analysis_report.txt
- Удалены неиспользуемые маски в mask/
- Удалены Zone.Identifier файлы

### Тесты
- 38/38 тестов проходят

## v0.1.0 - MVP (21.02.2026)

### Создано
- Структура проекта Flutter + FastAPI
- AR-экран с маской DIN для калибровки
- Экран измерения с симуляцией расчёта размеров
- Результаты измерений с отображением параметров
- Backend API с эндпоинтами измерения и подбора
- CV пайплайн (контурный анализ, детектор граней)
- Базовая модель данных замков
- Алгоритм matching с fuzzy tolerance

### Mobile App
- Главный экран с навигацией
- AR Camera экран с перетаскиваемой маской DIN
- Экран результатов измерений
- Модели: LockProfile, LockDimensions, CaptureContext

### Backend
- FastAPI приложение
- API: /api/v1/measure, /api/v1/match, /api/v1/locks
- Services: MeasurementService, MatchingService
- In-memory база замков (mock данные)

### CV Pipeline
- ContourAnalyzer - поиск контуров
- EdgeDetector - детектор границ
- GeometryCalculator - расчёт размеров в мм

### Документация
- 17 md файлов с ТЗ, архитектурой, планом
- Спецификация для AI агентов

### Сборка
- APK: build/app/outputs/flutter-apk/app-debug.apk (84MB)

## Следующие шаги
- Подключить реальный CV на OpenCV
- Обучить YOLO модель для детекции замков
- Подключить PostgreSQL базу
- Добавить реальный каталог замков
- Улучшить AR совмещение
- Тестирование на реальных замках
