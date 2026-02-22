# ================================================================================
# AI LOCK SELECTOR - STARTUP FILE
# ================================================================================
# Версия: 2.0.0
# Дата: 2026-02-22
# Проект: AI Lock Selector
# Репозиторий: https://github.com/cjpanches/ai_lock_selector
# Ветка: develop
# Оценка: 7.5/10
# ================================================================================

# ================================================================================
# 🚀 STARTUP PROMPT ДЛЯ OPENCODE (КОПИРОВАТЬ ИЗ OPENCODE_STARTUP.md)
# ================================================================================
# см. файл: /home/bot/porojects/ai_lock_project/OPENCODE_STARTUP.md
# ================================================================================

# ================================================================================
# 📁 РАСПОЛОЖЕНИЕ КЛЮЧЕВЫХ ФАЙЛОВ
# ================================================================================

"""
Основной путь проекта: /home/bot/porojects/ai_lock_project/

📋 ПЛАН РАЗРАБОТКИ:
  - /home/bot/porojects/ai_lock_project/OPENCODE_PROMPT.md     # Текущий план
  - /home/bot/porojects/ai_lock_project/OPENCODE_STARTUP.md     # Этот промпт

📊 СОСТОЯНИЕ ПРОЕКТА:
  - /home/bot/porojects/ai_lock_project/AI_EXPERTS/TECHNICAL_STATE.md  # Техническое состояние
  - /home/bot/porojects/ai_lock_project/AI_EXPERTS/EXPERT_INSTRUCTIONS.md  # Инструкции для экспертов
  - /home/bot/porojects/ai_lock_project/AI_EXPERTS/EXPERT_OUTPUT_TEMPLATE.md  # Шаблон вывода эксперта
  - /home/bot/porojects/ai_lock_project/PROJECT_STATE.md        # Состояние
  - /home/bot/porojects/ai_lock_project/SYSTEM_AUDIT.md         # Аудит

👥 AI ЭКСПЕРТЫ:
  - /home/bot/AI_EXPERTS/EXPERTS/KIMI/00_super_prompt.txt       # KIMI - Архитектор
  - /home/bot/AI_EXPERTS/EXPERTS/GROK/00_super_prompt.txt       # GROK - Анализ кода
  - /home/bot/AI_EXPERTS/EXPERTS/GPT/00_super_prompt.txt        # GPT - Генерация кода
  - /home/bot/AI_EXPERTS/EXPERTS/GEMINI/00_super_prompt.txt     # GEMINI - ML/CV
  - /home/bot/porojects/ai_lock_project/PROJECT_STATE.md        # Общее состояние
  - /home/bot/porojects/ai_lock_project/SYSTEM_AUDIT.md         # Аудит системы
  - /home/bot/porojects/ai_lock_project/CHANGELOG.md             # История версий

👥 ЭКСПЕРТНАЯ СИСТЕМА (AI_EXPERTS):
  - /home/bot/AI_EXPERTS/EXPERTS/KIMI/00_super_prompt.txt       # KIMI - Архитектор
  - /home/bot/AI_EXPERTS/EXPERTS/GROK/00_super_prompt.txt       # GROK - Анализ кода
  - /home/bot/AI_EXPERTS/EXPERTS/GPT/00_super_prompt.txt        # GPT - Генерация кода
  - /home/bot/AI_EXPERTS/EXPERTS/GEMINI/00_super_prompt.txt     # GEMINI - ML/CV

📱 MOBILE APP (Flutter):
  - /home/bot/porojects/ai_lock_project/mobile_app/lib/main.dart
  - /home/bot/porojects/ai_lock_project/mobile_app/lib/features/ar_camera/
  - /home/bot/porojects/ai_lock_project/mobile_app/pubspec.yaml

⚙️ BACKEND (FastAPI):
  - /home/bot/porojects/ai_lock_project/backend/app/main.py
  - /home/bot/porojects/ai_lock_project/backend/requirements.txt

🔬 CV PIPELINE (Python):
  - /home/bot/porojects/ai_lock_project/cv_pipeline/src/lock_pipeline.py
  - /home/bot/porojects/ai_lock_project/cv_pipeline/src/contour_analyzer.py
  - /home/bot/porojects/ai_lock_project/cv_pipeline/src/edge_detector.py
  - /home/bot/porojects/ai_lock_project/cv_pipeline/src/geometry_calculator.py
"""

# ================================================================================
# 📊 ТЕКУЩЕЕ СОСТОЯНИЕ ПРОЕКТА
# ================================================================================

"""
ОБЩАЯ ОЦЕНКА: 5.2/10

Компоненты:
| Компонент       | Оценка | Статус                    |
|-----------------|--------|---------------------------|
| Mobile App      | 4.5/10 | Требует Riverpod         |
| Backend         | 3.5/10 | Требует PostgreSQL       |
| CV Pipeline     | 3.0/10 | Требует YOLO             |
| Expert System   | 8/10   | ✅ Готов                  |
| Documentation   | 7/10   | ✅ Готов                  |

ТЕХНИЧЕСКИЙ ДОЛГ (приоритет порядок):
  P0: Riverpod в Flutter (plain setState сейчас)
  P0: Навигация go_router
  P0: PostgreSQL в backend
  P0: YOLO модель в CV
  P1: Unit тесты
  P1: Dataset (500+ фото)
  P2: CI/CD
"""

# ================================================================================
# 🎯 ТЕКУЩИЙ ШАГ РАЗРАБОТКИ
# ================================================================================

"""
ВЕРСИЯ: 1.0.7
ДАТА НАЧАЛА: 2026-02-22
ТЕКУЩИЙ ШАГ: #5 - CI/CD, UI/UX, Тесты (ЗАВЕРШЁН)

ЛОГ РАЗРАБОТКИ:
================
| Версия | Дата     | Шаг | Описание                                |
|--------|----------|-----|-----------------------------------------|
| 1.0.0  | 2026-02-22 | #1  | STARTUP файл создан                      |
| 1.0.1  | 2026-02-22 | #1  | Riverpod провайдеры созданы             |
| 1.0.2  | 2026-02-22 | #1  | GoRouter добавлен                       |
| 1.0.3  | 2026-02-22 | #2  | PostgreSQL + SQLAlchemy                 |
| 1.0.4  | 2026-02-22 | #2  | SQLite + seed данных                    |
| 1.0.5  | 2026-02-22 | #3  | CV Pipeline + YOLO                     |
| 1.0.6  | 2026-02-22 | #4  | Unit тесты                              |
| 1.0.7  | 2026-02-22 | #5  | CI/CD, UI/UX, доп. тесты              |

ЗАДАЧА #5: CI/CD, UI/UX, Тесты - ЗАВЕРШЕНО ✅
-----------------------------------------------
Статус: ГОТОВ
Дата: 2026-02-22

Выполнено:
  [x] 5.1 GitHub Actions CI/CD (.github/workflows/ci.yml) ✅
  [x] 5.2 Pre-commit hooks (.pre-commit-config.yaml) ✅
  [x] 5.3 UI/UX улучшения (анимации, glow effects) ✅
  [x] 5.4 Доп. тесты (API, Camera) ✅

Файлы:
  - .github/workflows/ci.yml
  - .pre-commit-config.yaml
  - mobile_app/lib/features/ar_camera/ar_camera_screen.dart (обновлён)
  - backend/tests/test_api.py
  - mobile_app/test/camera_provider_test.dart

ВСЕ ЗАДАЧИ ИЗ ПЛАНА ВЫПОЛНЕНЫ! ✅
=====================================

Следующий шаг: Свободная разработка
"""

# ================================================================================
# 🔗 СВЯЗИ ПРОЕКТА
# ================================================================================

"""
АРХИТЕКТУРА СИСТЕМЫ:
                    ┌──────────────────┐
                    │   Mobile App     │
                    │   (Flutter)      │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌─────────┐    ┌──────────┐   ┌─────────┐
        │  AR     │    │   CV     │   │ Backend │
        │ Camera  │───▶│ Pipeline │◀──│  API    │
        └─────────┘    └─────────┘   └────┬────┘
                                          │
                                   ┌───────▼───────┐
                                   │  PostgreSQL   │
                                   │   (нужно)     │
                                   └───────────────┘

ЗАВИСИМОСТИ:
  - Mobile → Backend: HTTP API (measure, match, locks)
  - Mobile → CV: GRPC или REST (обработка изображений)
  - CV → YOLO: Модель для детекции замка
  - Backend → PostgreSQL: Хранение каталога замков

КЛЮЧЕВЫЕ КОНСТАНТЫ:
  - DIN_CYLINDER_WIDTH = 10.0 mm
  - DIN_CYLINDER_HEIGHT = 17.0 mm
  - BACKSET_TOLERANCE = ±2.0 mm
  - CENTER_DISTANCE_TOLERANCE = ±3.0 mm
  - ЦЕЛЕВАЯ ТОЧНОСТЬ: ±1.5 mm

API ENDPOINTS:
  - POST /api/v1/measure   - Измерение параметров замка
  - POST /api/v1/match     - Подбор аналогов
  - GET  /api/v1/locks     - Список замков
"""

# ================================================================================
# 🛠 КОМАНДЫ ЗАПУСКА
# ================================================================================

"""
# Backend (FastAPI)
cd /home/bot/porojects/ai_lock_project/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Flutter (Development)
cd /home/bot/porojects/ai_lock_project/mobile_app
flutter pub get
flutter run

# Flutter (Build APK)
cd /home/bot/porojects/ai_lock_project/mobile_app
flutter build apk --debug

# Python CV Pipeline
cd /home/bot/porojects/ai_lock_project/cv_pipeline/src
python lock_pipeline.py

# Тесты
cd /home/bot/porojects/ai_lock_project/mobile_app
flutter test

# Lint
cd /home/bot/porojects/ai_lock_project/mobile_app
flutter analyze
"""

# ================================================================================
# 📝 ИНСТРУКЦИЯ ДЛЯ РАЗРАБОТЧИКА
# ================================================================================

"""
КАК НАЧАТЬ РАБОТУ С PROCODECODE:

1. Откройте новую сессию opencode
2. Скопируйте STARTUP PROMPT из шапки этого файла
3. Вставьте промпт в чат opencode
4. Продолжайте с того места, где остановились (те: #1)

КАкущий шагК ОБНОВИТЬ ЭТОТ ФАЙЛ:
  - После каждого завершённого шага добавляйте запись в лог
  - Обновляйте текущий шаг
  - Добавляйте новые ссылки при создании новых файлов

КОНВЕНЦИИ:
  - Dart: camelCase, Equatable, Riverpod
  - Python: pydantic, async/await, OpenCV
  - Файлы: snake_case
"""

# ================================================================================
# END OF STARTUP FILE
# ================================================================================
