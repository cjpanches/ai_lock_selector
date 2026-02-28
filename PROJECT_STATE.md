# AI LOCK SELECTOR - ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ==============================================
# Дата: 2026-02-23
# Версия: 4.3.0
# Статус: ✅ РАБОТАЕТ

---

## ОЦЕНКИ ЭКСПЕРТОВ (v4.3)

| Эксперт | Оценка | Комментарий |
|---------|--------|-------------|
| KIMI (Architecture) | 5.8/10 | Архитектура в целом |
| GROK (Code Analysis) | 5.8/10 | Code quality |
| GPT (Code Generation) | 5.5/10 | Генерация кода |
| GEMINI (ML/CV) | 5.5/10 | CV пайплайн |
| **MASTER** | **5.6/10** | Consensus |

---

## О ПРОЕКТЕ

**Название:** AI Lock Selector  
**Репозиторий:** https://github.com/cjpanches/ai_lock_selector  
**Ветка:** develop

---

## ТЕКУЩЕЕ СОСТОЯНИЕ (v4.3)

| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 6.5/10 | ✅ Работает (кнопка фото исправлена) |
| Backend | 6.0/10 | ✅ Работает |
| CV Pipeline | 5.0/10 | ✅ Готов к пре-разметке |
| Tests | 6/10 | ✅ 38 тестов |
| YOLO Dataset | В процессе | ⏳ Нужны фото |
| **Общая** | **5.5/10** | ✅ Работает |

---

## ЧТО РАБОТАЕТ

### Backend (FastAPI)
- ✅ REST API на localhost:8001
- ✅ SQLite база данных (147 замков)
- ✅ /api/v1/locks - получить все замки
- ✅ /api/v1/match - подбор аналогов
- ✅ /api/v1/measure - измерения
- ✅ Health check

### Flutter Web
- ✅ Главная страница (HomeScreen)
- ✅ Каталог замков (147 шт)
- ✅ AR камера с DIN маской
- ✅ Экран результатов
- ✅ GoRouter навигация

### CV Pipeline
- ✅ LockContourPipeline
- ✅ GeometryCalculator (исправлен)
- ✅ ContourAnalyzer
- ✅ EdgeDetector
- ✅ pre_label.py (пре-разметка для YOLO)
- ⚠️ YOLO не обучен

---

## КРИТИЧЕСКИЕ БАГИ

### Исправлены (v4.0):
- ✅ API matching - добавлен db parameter
- ✅ Router import - добавлен HomeScreen
- ✅ Division by zero - добавлена валидация
- ✅ GeometryCalculator - исправлены расчёты
- ✅ CORS - настроен

### Исправлены (v4.3):
- ✅ Кнопка фото - добавлен принудительный захват (long press)

---

## БАЗА ДАННЫХ

| Таблица | Записей |
|---------|----------|
| locks | 147 |
| manufacturers | 1 |
| lock_compatibility | 0 |
| measurements | 0 |

**Бренды:** Apecs, Avers

---

## ТЕХНОЛОГИЧЕСКИЙ СТЕК

### Frontend (Mobile)
- Flutter 3.41.2
- Riverpod 2.x
- go_router

### Backend
- FastAPI
- SQLite (aiosqlite)
- SQLAlchemy 2.0 async
- Pydantic v2

### CV Pipeline
- Python 3.x
- OpenCV 4.x
- YOLOv8 (структура готова)

---

## СБОР ДАННЫХ ДЛЯ YOLO

### Структура датасета
```
cv_pipeline/dataset/
├── images/
│   ├── train/      # Обучающие изображения
│   └── val/        # Валидационные изображения
├── labels/         # Аннотации YOLO формата
├── classes.txt     # 4 класса
└── lock_dataset.yaml
```

### Классы
| ID | Класс | Описание |
|----|-------|----------|
| 0 | lock_plate | Вся планка замка |
| 1 | cylinder_hole | Отверстие цилиндра (DIN) |
| 2 | mounting_hole | Крепёжные отверстия |
| 3 | handle_square | Квадрат ручки |

### Инструменты
- **pre_label.py** - скрипт пре-разметки (CV → YOLO)
- **Roboflow** - онлайн разметка (бесплатно до 1000 фото)
- **LabelImg** - десктоп разметка

### Текущий прогресс
- ✅ Структура датасета создана
- ✅ Скрипт пре-разметки работает
- ⏳ Нужны фото с правильного ракурса (500+)

---

## СЛЕДУЮЩИЕ ШАГИ

1. **Собрать 500+ фото замков** (правильный ракурс сверху)
2. **Разметить в Roboflow** (или использовать pre_label.py)
3. **Обучить YOLO** (100 эпох)
4. **Настроить PostgreSQL** для production

---

## КОМАНДЫ

### Backend
```bash
cd backend
DATABASE_URL=sqlite+aiosqlite:///./locks.db uvicorn app.main:app --port 8001
```

### Flutter Web
```bash
cd mobile_app
flutter build web
# затем запустить сервер
python3 -m http.server 8080
```

### Тесты
```bash
cd backend && pytest
```

---

## ФАЙЛЫ ДЛЯ ПРОДОЛЖЕНИЯ

- **Основной:** `PROJECT_STATE.md`
- **Стартовый:** `STARTUP.md`
- **Мастер:** `OPENCODE_STARTUP.md`
- **Эксперты:** `AI_EXPERTS/`

---

**Обновлено: 2026-02-23**
**Версия: 4.1.0**
**Статус: ✅ РАБОТАЕТ**
