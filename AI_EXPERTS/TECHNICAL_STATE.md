# AI LOCK SELECTOR - ТЕХНИЧЕСКОЕ СОСТОЯНИЕ ПРОЕКТА
# ====================================================
# Версия: 2.0.0
# Дата: 2026-02-22
# Статус: Активная разработка
# Ветка: develop
# ====================================================

## 1. ОБЩАЯ ИНФОРМАЦИЯ

**Название:** AI Lock Selector
**Репозиторий:** https://github.com/cjpanches/ai_lock_selector
**Описание:** Мобильное приложение для точного измерения параметров дверных замков через AR и подбора аналогов из каталога компании.
**Ветка:** develop
**Общая оценка:** 7.5/10 (повышена с 3.7/10)

---

## 2. СТРУКТУРА ПРОЕКТА

```
ai_lock_project/
├── mobile_app/                    # Flutter приложение
│   ├── lib/
│   │   ├── core/
│   │   │   ├── constants.dart
│   │   │   └── router.dart        # GoRouter конфигурация
│   │   ├── domain/
│   │   │   └── models/
│   │   │       └── capture_context.dart
│   │   ├── features/
│   │   │   ├── ar_camera/
│   │   │   │   └── ar_camera_screen.dart
│   │   │   └── measurement/
│   │   │       └── measurement_result_screen.dart
│   │   ├── providers/
│   │   │   ├── camera_provider.dart
│   │   │   ├── mask_provider.dart
│   │   │   ├── capture_provider.dart
│   │   │   ├── cv_provider.dart
│   │   │   └── providers.dart (barrel)
│   │   └── main.dart
│   ├── test/
│   │   ├── mask_provider_test.dart
│   │   ├── capture_provider_test.dart
│   │   └── camera_provider_test.dart
│   ├── pubspec.yaml
│   └── android/
│
├── backend/                       # FastAPI сервер
│   ├── app/
│   │   ├── api/
│   │   │   ├── locks.py          # CRUD для замков
│   │   │   ├── matching.py       # Подбор аналогов
│   │   │   ├── measurements.py   # Измерения
│   │   │   └── cv.py            # CV endpoints
│   │   ├── core/
│   │   │   └── config.py         # Настройки
│   │   ├── db/
│   │   │   ├── models.py         # SQLAlchemy модели
│   │   │   ├── database.py        # Async подключение
│   │   │   └── seed.py           # Начальные данные
│   │   ├── models/
│   │   │   └── schemas.py        # Pydantic схемы
│   │   ├── services/
│   │   │   ├── matching_service.py
│   │   │   └── measurement_service.py
│   │   ├── cv_service.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_matching.py
│   │   ├── test_schemas.py
│   │   ├── test_cv.py
│   │   └── test_api.py
│   ├── requirements.txt
│   └── pytest.ini
│
├── cv_pipeline/src/              # Computer Vision
│   ├── contour_analyzer.py       # Анализ контуров
│   ├── edge_detector.py          # Детекция границ
│   ├── geometry_calculator.py    # Геометрические вычисления
│   ├── lock_pipeline.py          # Основной пайплайн
│   └── yolo_detector.py          # YOLO детектор
│
├── .github/workflows/
│   └── ci.yml                    # GitHub Actions
│
├── .pre-commit-config.yaml
│
├── STARTUP.md                    # Стартовый файл
├── OPENCODE_PROMPT.md            # План разработки
├── PROJECT_STATE.md              # Состояние проекта
└── SYSTEM_AUDIT.md               # Аудит
```

---

## 3. ТЕХНОЛОГИЧЕСКИЙ СТЕК

### Frontend (Mobile)
- **Flutter:** 3.24+
- **Riverpod:** 2.4.9 (state management)
- **GoRouter:** 13.2.0 (навигация)
- **Camera:** 0.10.5+9
- **Dio:** 5.4.0 (HTTP client)
- **Material 3**

### Backend
- **FastAPI:** 0.109+
- **SQLAlchemy:** 2.0+ (async)
- **SQLite:** aiosqlite (вместо PostgreSQL для разработки)
- **Pydantic:** 2.5+
- **Uvicorn:** 0.27+

### CV Pipeline
- **Python:** 3.10+
- **OpenCV:** 4.9+
- **NumPy:** 1.26+
- **YOLOv8:** (опционально, wrapper готов)

### DevOps
- **GitHub Actions:** CI/CD
- **Pre-commit:** hooks
- **pytest:** тестирование

---

## 4. КОМПОНЕНТЫ И ИХ СОСТОЯНИЕ

### 4.1 Mobile App (Flutter)
| Компонент | Статус | Оценка |
|-----------|--------|--------|
| State Management (Riverpod) | ✅ Готов | 8/10 |
| Навигация (GoRouter) | ✅ Готов | 8/10 |
| AR Камера | ✅ Готов | 7/10 |
| UI/UX | ✅ Улучшен | 7/10 |
| Тесты | ⚠️ Частично | 5/10 |

### 4.2 Backend (FastAPI)
| Компонент | Статус | Оценка |
|-----------|--------|--------|
| Database (SQLite) | ✅ Готов | 7/10 |
| CRUD API | ✅ Готов | 8/10 |
| Matching Service | ✅ Готов | 7/10 |
| CV Integration | ✅ Готов | 6/10 |
| Тесты | ⚠️ Частично | 5/10 |

### 4.3 CV Pipeline
| Компонент | Статус | Оценка |
|-----------|--------|--------|
| Contour Analysis | ✅ Готов | 7/10 |
| Edge Detection | ✅ Готов | 7/10 |
| Geometry Calculator | ✅ Готов | 7/10 |
| YOLO Wrapper | ✅ Готов | 6/10 |
| Lock Pipeline | ✅ Готов | 7/10 |

### 4.4 DevOps
| Компонент | Статус | Оценка |
|-----------|--------|--------|
| CI/CD | ✅ Готов | 8/10 |
| Pre-commit | ✅ Готов | 7/10 |
| Тесты | ⚠️ Частично | 5/10 |

---

## 5. API ENDPOINTS

### Locks API
- `GET /api/v1/locks` — Список замков
- `GET /api/v1/locks/{id}` — Получить замок
- `POST /api/v1/locks` — Создать замок
- `PUT /api/v1/locks/{id}` — Обновить замок
- `DELETE /api/v1/locks/{id}` — Удалить замок

### Measurements API
- `POST /api/v1/measure` — Измерение параметров

### Matching API
- `POST /api/v1/match` — Подбор аналогов

### CV API
- `POST /api/v1/cv/process` — Обработка изображения
- `POST /api/v1/cv/detect` — Детекция замка

---

## 6. БАЗА ДАННЫХ

### Таблицы
- **manufacturers** — Производители (3 записи)
- **locks** — Замки (6 записей)
- **lock_compatibility** — Совместимость
- **measurements** — Измерения

### Seed Data
- 3 производителя: SecureLock, DoorGuard, SimpleLock
- 6 замков с различными типами

---

## 7. КЛЮЧЕВЫЕ КОНСТАНТЫ

### DIN Стандарт
- `DIN_CYLINDER_WIDTH = 10.0 mm`
- `DIN_CYLINDER_HEIGHT = 17.0 mm`

### Допуски (Fuzzy Matching)
- `BACKSET_TOLERANCE = ±2.0 mm`
- `CENTER_DISTANCE_TOLERANCE = ±3.0 mm`
- `PLATE_WIDTH_TOLERANCE = ±2.0 mm`
- `PLATE_HEIGHT_TOLERANCE = ±3.0 mm`

### Точность
- **Цель:** ±1.5 мм

---

## 8. КОМАНДЫ ЗАПУСКА

```bash
# Backend
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Flutter
cd mobile_app
flutter pub get
flutter run

# APK
cd mobile_app
flutter build apk --debug

# Тесты Flutter
cd mobile_app && flutter test

# Тесты Backend
cd backend && pytest

#Lint
cd mobile_app && flutter analyze
```

---

## 9. ЗАПУЩЕННЫЕ СЕРВИСЫ

- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **SQLite DB:** backend/locks.db

---

## 10. ЛОГ РАЗРАБОТКИ

| Версия | Дата | Шаг | Описание |
|--------|------|-----|----------|
| 1.0.0 | 2026-02-22 | #1 | STARTUP файл создан |
| 1.0.1 | 2026-02-22 | #1 | Riverpod провайдеры |
| 1.0.2 | 2026-02-22 | #1 | GoRouter |
| 1.0.3 | 2026-02-22 | #2 | SQLAlchemy |
| 1.0.4 | 2026-02-22 | #2 | SQLite + seed |
| 1.0.5 | 2026-02-22 | #3 | CV Pipeline |
| 1.0.6 | 2026-02-22 | #4 | Unit тесты |
| 1.0.7 | 2026-02-22 | #5 | CI/CD + UI |

---

## 11. ССЫЛКИ НА ФАЙЛЫ

### Основные
- STARTUP.md — Стартовый файл
- OPENCODE_PROMPT.md — План разработки
- PROJECT_STATE.md — Состояние проекта
- SYSTEM_AUDIT.md — Аудит

### AI Эксперты
- AI_EXPERTS/EXPERTS/KIMI/ — Архитектор
- AI_EXPERTS/EXPERTS/GROK/ — Анализ кода
- AI_EXPERTS/EXPERTS/GPT/ — Генерация кода
- AI_EXPERTS/EXPERTS/GEMINI/ — ML/CV

---

**Конец технического состояния**
