# Журнал разработки

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
