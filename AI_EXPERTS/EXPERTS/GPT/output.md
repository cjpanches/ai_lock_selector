# ЭКСПЕРТ: GPT (CODER)
# ======================================
# Дата: 2026-02-23
# Версия: 4.0.0
# Проект: AI Lock Selector
# ======================================

---

# ЧАСТЬ 1: АУДИТ ВСЕГО ПРОЕКТА

## ГЕНЕРАЦИЯ КОДА GPT
### Дата: 2026-02-23

---

## ОБЩАЯ ОЦЕНКА

**5.5/10**

Проект имеет хорошую архитектуру с разделение на Flutter frontend, FastAPI backend и CV pipeline, однако наблюдаются значительные проблемы с качеством кода, дублированием, отсутствием документации и слабым покрытием тестами. Многие задачи требуют ручной работы из-за сложности бизнес-логики.

---

## CODE CONVENTIONS

### Mobile App (Flutter)

**Оценка: 6/10**

**Соответствие конвенциям:**
- Используется Flutter Riverpod для state management
- Material 3 дизайн
- camelCase для переменных
- StatelessWidget для презентационных компонентов
- Используется Equatable для моделей (lock_profile.dart)

**Проблемы:**
1. **Дублирование кода LockType** - определён дважды:
   - `/mobile_app/lib/domain/models/lock.dart` (строки 1-46)
   - `/mobile_app/lib/features/catalog/catalog_screen.dart` (строки 159-193)
   
2. **Отсутствие единого стиля импортов** - в некоторых файлах относительные пути, в других абсолютные

3. **Провайдеры разделены, но часть логики в моделях** - `LocksResponse` и `ApiException` определены внутри `locks_provider.dart`, хотя должны быть в отдельных файлах

4. **Магические числа** - в `capture_provider.dart` строка 74: `150.0 * maskState.scale` без объяснения

5. **Неполная типизация** - в `ar_camera_screen.dart` строки 189-215: `final detections = result['detections'] as List;` без дженерик типа

**Рекомендации:**
- Вынести `LockType` в отдельный файл `domain/enums/lock_type.dart`
- Создать папку `domain/exceptions/` для кастомных исключений
- Добавить документацию для публичных методов провайдеров

---

### Backend (Python)

**Оценка: 5/10**

**Соответствие конвенциям:**
- Pydantic для валидации данных
- Async/await для I/O операций
- FastAPI для API
- Разделение на слои (api, services, db, models)
- Типизированные возвращаемые значения

**Проблемы:**
1. **Дублирование API endpoints** - `/api/v1/locks` определён в двух файлах:
   - `/backend/app/api/locks.py` (полный CRUD)
   - `/backend/app/api/measurements.py` (дублирующий функционал, строки 43-65)

2. **Несоответствие схем** - в `locks.py` строка 27 используется `lock_cylinder_hole`, но в `schemas.py` строка 63 поле называется `cylinder_hole`

3. **Неиспользуемые импорты** - в `matching_service.py` строка 2: `from typing import Optional` не используется

4. **Хардкод параметров** - в `measurement_service.py` строки 76-77 возвращаются захардкоженные значения `backset=55.0, center_distance=72.0` вместо реальных измерений

5. **Отсутствие error handling** - в `cv_service.py` строки 56-65 ошибки просто печатаются, но не логируются

6. **Неинициализированный scale_factor** - в `lock_pipeline.py` строка 41: `self.scale_factor: float = 0.0`, но используется до инициализации в `is_circular_hole` (строка 136)

**Рекомендации:**
- Удалить дублирующий код из `measurements.py`
- Исправить именование полей для согласованности
- Добавить логирование вместо print
- Реализовать реальный расчёт размеров вместо mock данных

---

### CV Pipeline

**Оценка: 6/10**

**Соответствие конвенциям:**
- dataclasses для структур данных
- Типизированные возвращаемые значения
- Разделение на логические модули (contour, edge, geometry, yolo)
- Docstrings для классов

**Проблемы:**
1. **Stub файлы не являются stub** - contour_analyzer.py, edge_detector.py, geometry_calculator.py уже имеют реализацию, но YOLO модель не обучена

2. **Проблема с импортами** - в `geometry_calculator.py` строки 116-117: импорты внутри функции, что затрудняет тестирование

3. **Дублирование констант** - `DIN_CYLINDER_WIDTH = 10.0` определён в:
   - `lock_pipeline.py` строка 29
   - `contour_analyzer.py` строка 19
   - `geometry_calculator.py` строка 7

4. **Хардкод в `estimate_thickness`** - `geometry_calculator.py` строка 54: возвращает всегда `3.0`

5. **Отсутствует валидация входных данных** - методы принимают None без проверки

**Рекомендации:**
- Создать общий конфиг файл с константами
- Вынести импорты на уровень модуля
- Реализовать расчёт толщины на основе анализа изображения

---

## REFACTORING OPPORTUNITIES

### High Priority (можно сделать генерацией)

| Файл | Проблема | Сложность |
|------|----------|-----------|
| `mobile_app/lib/features/catalog/catalog_screen.dart` | Дублирование LockType | Низкая |
| `mobile_app/lib/providers/locks_provider.dart` | ApiException/LocksResponse вне моделей | Низкая |
| `backend/app/api/measurements.py` | Дублирование endpoints из locks.py | Средняя |
| `backend/app/services/measurement_service.py` | Mock данные вместо реальных расчётов | Средняя |
| `cv_pipeline/src/geometry_calculator.py` | Импорты внутри функции | Низкая |
| `cv_pipeline/src/*.py` | Дублирование констант | Низкая |

### Low Priority

| Файл | Проблема | Сложность |
|------|----------|-----------|
| `backend/app/services/matching_service.py` | Неиспользуемые импорты | Низкая |
| `mobile_app/lib/providers/capture_provider.dart` | Магические числа | Низкая |
| `backend/app/cv_service.py` | print вместо logging | Низкая |
| `cv_pipeline/src/lock_pipeline.py` | Потенциальная ошибка с scale_factor | Средняя |

---

## TEST COVERAGE

| Компонент | Покрытие | Что нужно добавить |
|-----------|----------|-------------------|
| Mobile App | ~10% | Provider tests, Widget tests |
| Backend API | ~20% | Integration tests, Edge cases |
| Matching Service | ~40% | More match scenarios |
| CV Pipeline | ~15% | Image processing tests |
| Measurement Service | ~5% | Dimension calculation tests |

---

# ЧАСТЬ 2: АУДИТ СВОЕЙ ЗОНЫ (ГЕНЕРАЦИЯ КОДА)

## ГЕНЕРАЦИЯ КОДА GPT - ЗОНА ОТВЕТСТВЕННОСТИ
### Дата: 2026-02-23

---

## ЗАДАЧИ ДЛЯ АВТОМАТИЗАЦИИ

### Задачи которые можно решить генерацией кода:

1. **Создание unit-тестов для провайдеров** - тестирование state management логики
   - Причина: чёткая структура, предсказуемое поведение, легко покрыть моками

2. **Генерация boilerplate кода** - создание CRUD методов, DTO преобразований
   - Причина: повторяющиеся паттерны, формализованные правила

3. **Создание виджет-тестов для экранов** - тестирование UI компонентов
   - Причина: изолированные компоненты, можно мокать провайдеры

4. **Рефакторинг дублирующегося кода** - вынос LockType, констант
   - Причина: чёткие правила, легко автоматизировать поиск и замену

5. **Создание типовых сервисов** - генерация базовых методов для сервисов
   - Причина: стандартные паттерны (save, update, delete, find)

6. **Генерация mock данных для тестов** - создание фикстур
   - Причина: структура моделей известна, можно генерировать типовые данные

### Задачи которые требуют ручной работы:

1. **Реализация CV алгоритмов** - реальный контурный анализ, детекция отверстий
   - Причина: требует экспертных знаний в Computer Vision, понимания физики замков

2. **Обучение YOLO модели** - создание датасета, разметка, тренировка
   - Причина: требует большого количества размеченных данных, GPU ресурсов

3. **Интеграция с PostgreSQL** - настройка БД, миграции, заполнение данных
   - Причина: требует понимания инфраструктуры, ручной настройки

4. **Исправление бизнес-логики** - захардкоженные значения в measurement_service.py
   - Причина: требует понимания domain knowledge - как правильно измерять замки

5. **UX/UI доработки** - улучшение визуальной маски, анимации
   - Причина: требует дизайнерского мышления, тестирования с пользователями

6. **Калибровка точности** - настройка tolerance параметров для matching
   - Причина: требует тестирования на реальных данных, итеративной настройки

---

## КОНКРЕТНЫЕ ФАЙЛЫ ДЛЯ РЕФАКТОРИНГА

### Файл 1: LockType (дублирование)

**Путь:** 
- `/home/bot/porojects/ai_lock_project/mobile_app/lib/domain/models/lock.dart` (строки 1-46)
- `/home/bot/porojects/ai_lock_project/mobile_app/lib/features/catalog/catalog_screen.dart` (строки 159-193)

**Проблемы:**
- LockType определён дважды с одинаковой логикой
- Нет единого источника истины
- Изменения нужно вносить в двух местах

**Рекомендуемый рефакторинг:**
1. Создать файл `mobile_app/lib/domain/enums/lock_type.dart` с единым определением
2. Экспортировать из `mobile_app/lib/domain/models/lock.dart`
3. Удалить дубликат из `catalog_screen.dart`
4. Импортировать из нового места

---

### Файл 2: measurements.py (дублирование API)

**Путь:** `/home/bot/porojects/ai_lock_project/backend/app/api/measurements.py`

**Проблемы:**
- Дублирует функциональность `/api/v1/locks` (строки 43-65)
- Использует глобальные переменные `matching_service` без dependency injection
- Не использует БД сессию из Depends

**Рекомендуемый рефакторинг:**
1. Удалить endpoints `/`, `/{lock_id}` из measurements.py
2. Оставить только `/measure` и `/match`
3. Добавить dependency injection для сервисов

---

### Файл 3: measurement_service.py (mock данные)

**Путь:** `/home/bot/porojects/ai_lock_project/backend/app/services/measurement_service.py`

**Проблемы:**
- Строки 76-77: возвращаются захардкоженные значения `backset=55.0, center_distance=72.0`
- Реальный расчёт не выполняется - контуры находятся, но не используются
- `_find_plate_contour` находит контур, но размеры рассчитываются неправильно

**Рекомендуемый рефакторинг:**
1. Использовать найденный контур планки для реального расчёта backset
2. Вычислить center_distance на основе позиции цилиндра и ручки
3. Использовать крепёжные отверстия для уточнения размеров

---

### Файл 4: CV Pipeline константы

**Путь:** 
- `/home/bot/porojects/ai_lock_project/cv_pipeline/src/lock_pipeline.py`
- `/home/bot/porojects/ai_lock_project/cv_pipeline/src/contour_analyzer.py`
- `/home/bot/porojects/ai_lock_project/cv_pipeline/src/geometry_calculator.py`

**Проблемы:**
- `DIN_CYLINDER_WIDTH = 10.0` дублируется в 3 файлах
- При изменении придётся менять в нескольких местах
- Нет центрального конфига

**Рекомендуемый рефакторинг:**
1. Создать `cv_pipeline/src/config.py` с общими константами
2. Импортировать оттуда во все модули
3. Добавить type hints и документацию

---

## TEST IMPROVEMENTS

### Что можно сгенерировать:

| Тест | Файл | Сложность |
|------|------|-----------|
| Provider unit tests | mobile_app/lib/providers/*.dart | Низкая |
| Widget tests для экранов | mobile_app/lib/features/*/*.dart | Средняя |
| API integration tests | backend/app/api/*.py | Средняя |
| Schema validation tests | backend/app/models/schemas.py | Низкая |
| Service unit tests | backend/app/services/*.py | Средняя |

### Примеры конкретных тестов для генерации:

1. **locks_provider_test.dart** - тестирование fetchLocks, fetchLock, фильтрации
2. **camera_provider_test.dart** - тестирование инициализации камеры
3. **mask_provider_test.dart** - тестирование updatePosition, updateScale, auto-detection
4. **matching_service_test.py** - тесты на разные сценарии matching
5. **lock_pipeline_test.py** - тесты CV пайплайна на synthetic данных

---

## РЕКОМЕНДАЦИИ ПО ЗОНЕ GPT

### Конкретные рекомендации по улучшению кода:

1. **Внедрить строгую типизацию в Flutter**
   - Добавить анализ в pubspec.yaml: `analyzer: { errors: { invalid_annotation_target: warning } }`
   - Использовать `late` ключевое слово для полей инициализируемых в конструкторе

2. **Добавить null safety в Python с mypy**
   - Создать mypy.ini с конфигурацией
   - Типизировать все функции в backend/app/

3. **Улучшить обработку ошибок**
   - Заменить все `print()` на `logging`
   - Добавить structured logging с контекстом

4. **Создать общие утилиты**
   - Вынести магические числа в константы
   - Создать `constants.dart` в core/
   - Создать `config.py` в cv_pipeline/

5. **Добавить документацию**
   - Swagger для API (уже есть, но можно улучшить описания)
   - docstring для всех публичных методов

### Что можно автоматизировать:

1. Генерация тестов на основе структуры моделей
2. Создание CRUD boilerplate для новых сущностей
3. Проверка code style (linter, formatter)
4. Генерация mock данных из схем

### Что требует ручной работы:

1. CV алгоритмы (детекция, сегментация)
2. Обучение ML моделей
3. UX/UI решения
4. Интеграция с внешними системами
5. Performance optimization
6. Security audit

---

**Итог:** Проект имеет хорошую базу, но требует значительной работы по устранению дублирования, улучшению тестового покрытия и доработке бизнес-логики. Около 40% задач по рефакторингу можно автоматизировать, остальные требуют экспертного участия.
