# AI LOCK SELECTOR - ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ==============================================
# Дата: 2026-02-22
# Версия: 2.0.0
# Статус: Активная разработка

---

## О ПРОЕКТЕ

**Название:** AI Lock Selector  
**Репозиторий:** https://github.com/cjpanches/ai_lock_selector  
**Ветка:** develop

Мобильное приложение для точного измерения параметров дверных замков через AR и подбора аналогов из каталога компании.

---

## ТЕКУЩАЯ ОЦЕНКА

| Компонент | Оценка | Проблемы |
|-----------|--------|----------|
| Mobile (Flutter) | 4.5/10 | Riverpod, Navigation |
| Backend (FastAPI) | 3.5/10 | PostgreSQL, миграции |
| CV Pipeline | 3.0/10 | STUB файлы |
| **Общая** | **3.7/10** | Требует доработки |

---

## ТЕХНОЛОГИЧЕСКИЙ СТЕК

### Frontend (Mobile)
- Flutter 3.24+
- Riverpod 2.x (требует внедрения)
- go_router / auto_route (требует внедрения)
- ARCore / ARKit
- Camera package

### Backend
- FastAPI 0.110+
- PostgreSQL 16+ (требует внедрения)
- SQLAlchemy 2.0 async
- Alembic (миграции)
- Pydantic v2

### CV Pipeline
- Python 3.10-3.12
- OpenCV 4.10+
- YOLOv8 / YOLOv11
- torch 2.4+
- NumPy, SciPy

### AI Экспертная Система
- 4 эксперта: GROK, KIMI, GPT, GEMINI
- ORCHESTRATOR - координатор
- CROSS_EXPERT - синтез

---

## СТРУКТУРА ПРОЕКТА

```
ai_lock_selector/
├── mobile_app/              # Flutter приложение
├── backend/                 # FastAPI сервер
├── cv_pipeline/             # Компьютерное зрение
├── AI_EXPERTS/             # AI экспертная система
│   ├── EXPERTS/            # 4 эксперта
│   │   ├── GROK/          # Анализ кода + автоматизация
│   │   ├── KIMI/          # Архитектура + планирование
│   │   ├── GPT/           # Генерация кода
│   │   └── GEMINI/        # ML/CV
│   ├── CROSS_EXPERT/      # Коллективный анализ
│   ├── FACT/              # Текущее состояние
│   ├── IDEAL_PLAN/        # Целевая архитектура
│   ├── ORCHESTRATOR/      # Координатор
│   └── requirements.txt
└── docs/                   # Спецификации
```

---

## AI ЭКСПЕРТНАЯ СИСТЕМА

### Эксперты и их роли

#### GROK (GROK_CODE_ANALYZER)
- **Роль:** Анализ кода, оптимизация CV, автоматизация
- **Компетенции:**
  - Code Analysis
  - Bug Detection
  - CV Optimization
  - Performance
  - Automation
  - Workflow Optimization
- **Зависимости:** KIMI (архитектура)

#### KIMI (KIMI_ARCHITECT)
- **Роль:** Архитектура, стратегическое планирование, координация
- **Компетенции:**
  - Architecture Design
  - Tech Planning
  - Risk Assessment
  - Cross-Expert Coordination
  - Workflow Optimization
- **Зависимости:** GROK, GPT, GEMINI

#### GPT (GPT_CODER)
- **Роль:** Генерация и рефакторинг кода
- **Компетенции:**
  - Code Generation
  - Refactoring
  - Test Generation
  - Snippets Creation
- **Зависимости:** KIMI (архитектура)

#### GEMINI (GEMINI_ML_EXPERT)
- **Роль:** Машинное обучение и компьютерное зрение
- **Компетенции:**
  - ML Model Design
  - CV Optimization
  - Dataset Curation
- **Зависимости:** GROK (анализ кода)

### Файлы суперпромтов
- `AI_EXPERTS/EXPERTS/GROK/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/KIMI/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/GPT/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/GEMINI/00_super_prompt.txt`

---

## ПРИОРИТЕТЫ РАЗРАБОТКИ

### P0 - Критические
1. **Riverpod 2.x** - правильная структура провайдеров
2. **Навигация** - go_router / auto_route / typed routes
3. **PostgreSQL** - миграции, индексы, connection pool

### P1 - Высокие
4. **CV Pipeline** - точность ±1.5 мм, робастность
5. **YOLOv8** - интеграция, dataset
6. **Производительность** - AR + CV inference

### P2 - Средние
7. **CI/CD** - GitHub Actions, pre-commit hooks
8. **Тесты** - покрытие >70%

### P3 - Низкие
9. **Backend** - rate limiting, caching, logging

---

## ПЛАН ОПТИМИЗАЦИИ

### Цель
Повысить общую оценку с 3.7/10 до 8+/10

### Этапы

#### Этап 1: Фундамент (Недели 1-2)
- KIMI: Архитектура Riverpod
- GPT: Базовые провайдеры
- GROK: PostgreSQL схема + миграции

#### Этап 2: CV Pipeline (Недели 3-4)
- GEMINI: contour_analyzer + edge_detector
- GROK: Оптимизация

#### Этап 3: Интеграция (Недели 5-6)
- GEMINI: YOLOv8
- GPT: AR → CV мост

#### Этап 4: Стабилизация (Недели 7-8)
- Все: Тесты
- GROK: CI/CD

---

## РАБОТА С AI ЭКСПЕРТАМИ

### Протокол обмена данными

1. **Создание задачи для эксперта:**
   - Создать временный файл с промптом в `AI_EXPERTS/TEMP/`
   - Отправить в соответствующий AI (GROK/KIMI/GPT/GEMINI)
   - Получить ответ

2. **Запись ответа эксперта:**
   - Записать ответ в `AI_EXPERTS/EXPERTS/[EXPERT]/00_super_prompt.txt`
   - Обновить `AI_EXPERTS/CROSS_EXPERT/` при необходимости

3. **Синтез экспертов:**
   - KIMI собирает мнения всех экспертов
   - Создаётся сводный план в `CROSS_EXPERT/`

### Метрики успеха

| Метрика | Текущее | Целевое |
|---------|---------|---------|
| CV точность | ±2-3 мм | ±1.5 мм |
| AR FPS | <30 | >30 |
| API response | - | <200ms |
| Покрытие тестами | 0% | >70% |

---

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### DIN Стандарт
- DIN_CYLINDER_WIDTH = 10.0 mm
- DIN_CYLINDER_HEIGHT = 17.0 mm

### Допуски (Fuzzy Matching)
- BACKSET_TOLERANCE = ±2.0 mm
- CENTER_DISTANCE_TOLERANCE = ±3.0 mm
- PLATE_WIDTH_TOLERANCE = ±2.0 mm
- PLATE_HEIGHT_TOLERANCE = ±3.0 mm

### API Endpoints
```
POST /api/v1/measure   - Измерение параметров замка
POST /api/v1/match     - Подбор аналогов
GET  /api/v1/locks     - Список замков
```

---

## КОМАНДЫ ЗАПУСКА

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile App
```bash
cd mobile_app
flutter pub get
flutter run
```

### Build APK
```bash
cd mobile_app
flutter build apk --debug
```

---

## КОНВЕНЦИИ КОДА

### Dart
- Использовать Equatable для моделей
- camelCase для переменных
- flutter_riverpod для state

### Python
- pydantic для моделей
- async/await для I/O
- OpenCV для CV

---

## СЛЕДУЮЩИЕ ШАГИ

1. Запустить анализ кода через GROK
2. Получить архитектурные рекомендации от KIMI
3. Начать внедрение Riverpod через GPT
4. Запустить CV Pipeline через GEMINI

---

**Документ создан для открытия проекта в OpenCode**
**Обновлено: 2026-02-22**
