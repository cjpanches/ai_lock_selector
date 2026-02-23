# AI LOCK SELECTOR - ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ==============================================
# Дата: 2026-02-23
# Версия: 4.0.0
# Статус: Требуются критические исправления

---

## ОЦЕНКИ ЭКСПЕРТОВ (v4.0.0)

| Эксперт | Оценка | Комментарий |
|---------|--------|-------------|
| KIMI (Architecture) | 5.5/10 | Критические баги, технический долг |
| GROK (Code Analysis) | 5.8/10 | 3 critical бага |
| GPT (Code Generation) | 5.5/10 | Дублирование, тесты |
| GEMINI (ML/CV) | 4/10 | YOLO не обучен, сломан |
| **MASTER** | **5.2/10** | Consensus - требуются исправления |

---

## О ПРОЕКТЕ

**Название:** AI Lock Selector  
**Репозиторий:** https://github.com/cjpanches/ai_lock_selector  
**Ветка:** develop

Мобильное приложение для точного измерения параметров дверных замков через AR и подбора аналогов из каталога компании.

---

## ТЕКУЩАЯ ОЦЕНКА (ПОСЛЕ АУДИТА v4.0)

| Компонент | Оценка | Статус | Проблемы |
|-----------|--------|--------|----------|
| Mobile App | 6.1/10 | ⚠️ | Router import, hardcoded URLs |
| Backend | 5.4/10 | 🔴 CRITICAL | API matching crash, CORS |
| CV Pipeline | 5.4/10 | 🔴 BROKEN | GeometryCalculator stub, YOLO |
| Tests | 3/10 | ❌ | Минимальное покрытие |
| **Общая** | **5.2/10** | 🔴 НЕ РАБОТАЕТ | Критические баги |

---

## КРИТИЧЕСКИЕ БАГИ (P0 - ТРЕБУЮТ НЕМЕДЛЕННОГО ИСПРАВЛЕНИЯ)

### 1. API Matching Crash 🔴 CRITICAL
**Файлы:** 
- `backend/app/api/matching.py:14` - missing `db` parameter
- `backend/app/api/measurements.py:38` - missing `db` parameter

**Влияние:** API endpoints падают с 500 ошибкой

**Исправление:**
```python
# Добавить в функцию:
db: AsyncSession = Depends(get_db)
# И передать в matching_service.find_matches(profile, db)
```

### 2. Router Import Missing 🔴 CRITICAL
**Файл:** `mobile_app/lib/core/router.dart:3`
**Влияние:** Приложение не запускается

**Исправление:** Добавить `import '../features/home/home_screen.dart';`

### 3. Division by Zero 🟠 HIGH
**Файл:** `cv_pipeline/src/lock_pipeline.py:136`
**Влияние:** Runtime crash при scale_factor=0

**Исправление:**
```python
if self.scale_factor > 0:
    diameter_mm = diameter_px / self.scale_factor
```

### 4. GeometryCalculator Broken 🟠 HIGH
**Файлы:** 
- `cv_pipeline/src/geometry_calculator.py:54` - estimate_thickness() returns 3.0 stub
- `cv_pipeline/src/geometry_calculator.py:158` - center_distance = backset (incorrect)

**Влияние:** Неправильные измерения

---

## ВЫПОЛНЕННЫЕ ЗАДАЧИ

### v3.x серия:
1. ✅ PostgreSQL миграция (docker-compose)
2. ✅ Flutter Catalog Screen
3. ✅ YOLO Integration (структура готова)
4. ✅ База данных замков (147 замков)
5. ✅ P0 Bug Fixes (base64, camera dimensions)
6. ✅ P2 Refactoring (DINMaskPainter, Equatable)
7. ✅ DIN Mask Fix (точная маска по euro_profile_exact.svg)

---

## ТЕХНОЛОГИЧЕСКИЙ СТЕК

### Frontend (Mobile)
- Flutter 3.24+
- Riverpod 2.x
- go_router
- camera package

### Backend
- FastAPI 0.110+
- PostgreSQL 16 / SQLite (для тестов)
- SQLAlchemy 2.0 async
- Pydantic v2

### CV Pipeline
- Python 3.10-3.12
- OpenCV 4.x
- YOLOv8 (ТРЕБУЕТ ОБУЧЕНИЯ)

---

## СТРУКТУРА ПРОЕКТА

```
ai_lock_selector/
├── mobile_app/              # Flutter приложение
├── backend/                 # FastAPI сервер
├── cv_pipeline/             # Компьютерное зрение
│   ├── dataset/            # YOLO датасет (пустой)
│   └── src/               # CV модули
├── datafordb/              # Данные для БД
├── mask/                   # Чертежи и маски
├── AI_EXPERTS/             # AI экспертная система
└── docker-compose.yml       # PostgreSQL
```

---

## ТЕСТЫ

```
Backend: 23/23 ✅ (но есть баги в API)
```

---

## СЛЕДУЮЩИЕ ШАГИ

### P0 (Немедленно - Исправить чтобы работало):
1. 🔴 Исправить API matching (добавить db parameter)
2. 🔴 Исправить Router import (добавить HomeScreen)
3. 🔴 Исправить division by zero в CV
4. 🔴 Исправить GeometryCalculator

### P1 (Следующий спринт):
5. 🟠 Исправить CORS security
6. 🟠 Убрать mock данные из measurement_service
7. 🟠 Добавить тесты

### P2 (Долгосрочный):
8. Обучить YOLO модель (500+ фото)
9. Рефакторинг кода
10. Улучшить архитектуру

---

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### DIN Стандарт (евроцилиндр)
- **EURO_CYLINDER_HOLE = 33×17 mm**
- Верхний полукруг: диаметр 17mm
- Щель: ширина 10mm
- Нижний полукруг: радиус 5mm
- Общая высота: 33mm

### Допуски (ТРЕБУЕТ УЛУЧШЕНИЯ)
- BACKSET_TOLERANCE = ±2.0 mm (цель: ±1.5mm)
- CENTER_DISTANCE_TOLERANCE = ±3.0 mm (цель: ±1.5mm)
- PLATE_WIDTH_TOLERANCE = ±2.0 mm
- PLATE_HEIGHT_TOLERANCE = ±3.0 mm

---

## КОМАНДЫ ЗАПУСКА

### Backend
```bash
cd backend && uvicorn app.main:app --reload
```

### Mobile App
```bash
cd mobile_app && flutter run
```

### Тесты
```bash
cd backend && pytest
```

### Build APK
```bash
cd mobile_app && flutter build apk --debug
```

---

## ФАЙЛЫ ДЛЯ ПРОДОЛЖЕНИЯ

- **Основной:** `PROJECT_STATE.md` (этот файл)
- **Стартовый:** `STARTUP.md`
- **Мастер:** `OPENCODE_MASTER_PROMPT.txt`
- **Чертёж:** `mask/euro_profile_exact.svg`

---

**Обновлено: 2026-02-23**
**Версия: 4.0.0**
**Статус: Требуются критические исправления P0**
