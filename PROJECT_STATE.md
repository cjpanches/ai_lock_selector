# AI LOCK SELECTOR - ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ==============================================
# Дата: 2026-02-23
# Версия: 3.1.0
# Статус: DIN маска исправлена

---

## ОЦЕНКИ ЭКСПЕРТОВ (v3.0.0)

| Эксперт | Оценка | Комментарий |
|---------|--------|-------------|
| KIMI (Architecture) | 6.5/10 | Координатные баги |
| GROK (Code Analysis) | 5.0/10 | Критические баги |
| GPT (Code Generation) | 6.5/10 | SRP нарушения |
| GEMINI (ML/CV) | 6.0/10 | YOLO не загружен |
| **MASTER** | **6.5/10** | Consensus |

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
| Mobile App | 7.8/10 | ✅ Готов |
| Backend | 7.2/10 | ✅ Готов |
| CV Pipeline | 6.0/10 | ⚠️ Нужен YOLO |
| Manual Alignment | 8.0/10 | ✅ Готов (пользователь подтверждает) |
| **Общая** | **7.5/10** | В разработке |

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

### 5. P0 Bug Fixes (v3.0.2) ✅
- Исправлен base64 encoding: `bytes.toString()` → `base64Encode(bytes)`
- Исправлены размеры preview камеры: swap width/height
- Проверен focal point delta: код корректный
- Добавлены unit тесты для MaskNotifier

### 6. P2 Refactoring (v3.0.4) ✅
- Извлечён DINMaskPainter в отдельный файл
- Добавлен Equatable в MaskState и CaptureState
- Улучшена модульность и maintainability

### 7. DIN Mask Fix (v3.1.0) ✅
- Маска перерисована точно по чертежу `euro_profile_exact.svg`
- Использованы точные координаты:
  - Общая высота: 33mm
  - Верхний полукруг: диаметр 17mm (радиус 8.5mm)
  - Щель шириной: 10mm (x: 11.5 - 21.5mm)
  - Нижний полукруг: радиус 5mm
- Размер маски: 60×120px (соответствует 17×33mm)
- Упрощён UI - ручное подтверждение совмещения пользователем

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
├── mask/                   # Чертежи и маски
│   └── euro_profile_exact.svg  # Эталонная маска DIN
├── AI_EXPERTS/             # AI экспертная система
└── docker-compose.yml       # PostgreSQL
```

---

## ТЕСТЫ

```
Backend: 23/23 ✅
```

---

## СЛЕДУЮЩИЕ ШАГИ

### P1 (High):
1. ~~PostgreSQL миграция~~ ✅
2. ~~База данных замков~~ ✅
3. ~~Flutter catalog screen~~ ✅
4. ~~Camera integration (AR камера)~~ ✅
5. ~~DIN маска исправлена (ручное совмещение)~~ ✅

### P2 (Medium):
6. YOLO dataset collection (500+ фото) - требует ручного сбора
7. YOLO training
8. Flutter widget tests
9. Documentation

---

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### DIN Стандарт (евроцилиндр)
- **EURO_CYLINDER_HOLE = 33×17 mm** (используется как маска)
- Верхний полукруг: диаметр 17mm, радиус 8.5mm
- Щель: ширина 10mm (x: 11.5 - 21.5mm)
- Нижний полукруг: радиус 5mm
- Общая высота: 33mm
- Точка пересечения: y = 15.37386mm

### Файл маски
- `mask/euro_profile_exact.svg` - эталонный чертёж
- Координаты в mm точно соответствуют размерам

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
- **Чертёж маски:** `mask/euro_profile_exact.svg`

---

**Обновлено: 2026-02-23**
