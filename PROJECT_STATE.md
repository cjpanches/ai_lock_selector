# AI LOCK SELECTOR - ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ==============================================
# Дата: 2026-02-22
# Версия: 3.0.0
# Статус: Активная разработка

---

## О ПРОЕКТЕ

**Название:** AI Lock Selector  
**Репозиторий:** https://github.com/cjpanches/ai_lock_selector  
**Ветка:** develop

Мобильное приложение для точного измерения параметров дверных замков через AR и подбора аналогов из каталога компании.

---

## ТЕКУЩАЯ ОЦЕНКА

| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.0/10 | ✅ Готов |
| Backend | 7.2/10 | ✅ Готов |
| CV Pipeline | 6.0/10 | ⚠️ Нужен YOLO |
| **Общая** | **6.8/10** | В разработке |

---

## ВЫПОЛНЕННЫЕ ЗАДАЧИ

### 1. PostgreSQL миграция (P0) ✅
- Создан `.env.example` с PostgreSQL конфигом
- Создан `docker-compose.yml` для PostgreSQL
- Обновлён `config.py` для поддержки SQLite/PostgreSQL

### 2. Flutter Catalog Screen (P1) ✅
- Создан `mobile_app/lib/domain/models/lock.dart`
- Создан `mobile_app/lib/providers/locks_provider.dart`
- Создан `mobile_app/lib/features/catalog/catalog_screen.dart`
- Обновлён роутер

### 3. YOLO Integration (P0) ✅
- Создана структура датасета `cv_pipeline/dataset/`
- Создан `cv_pipeline/train_yolo.py`
- Создан `cv_pipeline/src/enhanced_pipeline.py`
- YOLO требует ручной сбор 500+ фото

### 4. База данных замков (P1) ✅
- Создан парсер HTML `datafordb/parser_final.py`
- Экспорт в CSV `datafordb/locks_final.csv` (181 замок)
- Импорт в БД - **147 замков**
- Обновлены модели БД с новыми полями:
  - `lock_cylinder_hole` = "33x17" (отверстие под евроцилиндр)
  - `description` - описание серии
  - `series`, `color` - серия, цвет
  - `package_type`, `package_qty`, `minibox_qty` - упаковка
  - `purpose`, `for_entry_doors`, `for_interior_doors` - назначение
  - `bolt_*`, `mechanism_type`, `key_*`, `cylinder_*` - тех. параметры

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
- YOLOv8 (требует обучения)

---

## СТРУКТУРА ПРОЕКТА

```
ai_lock_selector/
├── mobile_app/              # Flutter приложение
├── backend/                 # FastAPI сервер
├── cv_pipeline/             # Компьютерное зрение
│   ├── dataset/            # YOLO датасет
│   └── src/               # CV модули
├── datafordb/              # Данные для БД
│   └── locks_final.csv     # 181 замок
├── AI_EXPERTS/             # AI экспертная система
└── docker-compose.yml       # PostgreSQL
```

---

## ТЕСТЫ

```
Backend: 23/23 ✅
```

---

## СЛЕДУЮЩИЕ ШАГИ (по KIMI)

### P0 (Critical):
1. ~~PostgreSQL миграция~~ ✅
2. ~~База данных замков~~ ✅
3. YOLO dataset collection (500+ фото) - требует ручного сбора
4. YOLO training

### P1 (High):
5. Flutter catalog screen ✅
6. Camera integration (AR камера)

### P2 (Medium):
7. Flutter widget tests
8. Type hints
9. Documentation

---

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### DIN Стандарт
- DIN_CYLINDER_WIDTH = 10.0 mm
- DIN_CYLINDER_HEIGHT = 17.0 mm
- **EURO_CYLINDER_HOLE = 33x17 mm** (используется как маска)

### Допуски (Fuzzy Matching)
- BACKSET_TOLERANCE = ±2.0 mm
- CENTER_DISTANCE_TOLERANCE = ±3.0 mm
- PLATE_WIDTH_TOLERANCE = ±2.0 mm
- PLATE_HEIGHT_TOLERANCE = ±3.0 mm

---

## КОМАНДЫ ЗАПУСКА

### Backend
```bash
# С PostgreSQL
docker-compose up -d postgres
cp backend/.env.example backend/.env
cd backend && uvicorn app.main:app --reload

# Тесты
cd backend && pytest
```

### Mobile App
```bash
cd mobile_app
flutter pub get
flutter run
```

---

## ФАЙЛЫ ДЛЯ ПРОДОЛЖЕНИЯ

- **Этот файл:** `PROJECT_STATE.md`
- **Стартовый промт:** `OPENCODE_STARTUP.md`
- **Мастер промт:** `OPENCODE_MASTER_PROMPT.txt`

---

**Обновлено: 2026-02-22**
