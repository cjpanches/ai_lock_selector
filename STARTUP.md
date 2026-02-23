# ================================================================================
# AI LOCK SELECTOR - STARTUP FILE
# ================================================================================
# Версия: 4.0.0
# Дата: 2026-02-23
# Проект: AI Lock Selector
# Репозиторий: https://github.com/cjpanches/ai_lock_selector
# Ветка: develop
# Оценка: 5.2/10 (требуются критические исправления)
# ================================================================================

# ================================================================================
# 🚀 STARTUP PROMPT - СКОПИРУЙТЕ В OPENCODE
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ (в порядке приоритета):
1. STARTUP.md - этот файл (стартовые инструкции)
2. OPENCODE_MASTER_PROMPT.txt - мастер промт для OpenCode
3. PROJECT_STATE.md - текущее состояние проекта
4. AI_EXPERTS/MASTER_ANALYSIS_v3.md - анализ экспертов

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite/PostgreSQL, порт 8000)
- cv_pipeline/src/ - Computer Vision (OpenCV + YOLO)
- AI_EXPERTS/ - Экспертная система

## ТЕКУЩЕЕ СОСТОЯНИЕ (v4.0.0):
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 6.1/10 | ⚠️ Router import missing |
| Backend | 5.4/10 | 🔴 API matching crash |
| CV Pipeline | 5.4/10 | 🔴 GeometryCalculator broken |
| Tests | 3/10 | ❌ Минимальное покрытие |
| **Общая** | **5.2/10** | 🔴 НЕ РАБОТАЕТ |

## КРИТИЧЕСКИЕ БАГИ (P0):
1. 🔴 API matching crash - missing `db` parameter
2. 🔴 Router import missing - HomeScreen not imported  
3. 🔴 Division by zero - scale_factor validation missing
4. 🔴 GeometryCalculator broken - stub values

## ВЫПОЛНЕННЫЕ ЗАДАЧИ:
1. ✅ PostgreSQL миграция
2. ✅ Flutter Catalog Screen
3. ✅ YOLO интеграция (структура)
4. ✅ База данных замков (147 шт)
5. ✅ P0 баги исправлены (v3.x)
6. ✅ DIN маска исправлена

## ПРИОРИТЕТЫ:
1. P0: Исправить критические баги (чтобы работало)
2. P1: Добавить тесты, исправить CORS
3. P2: Обучить YOLO, рефакторинг

## ГЛАВНЫЕ РИСКИ:
- API падает (matching endpoints)
- CV возвращает неверные данные (stub)
- Нет YOLO модели

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
APK: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter build apk --debug
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## AI ЭКСПЕРТЫ - ФАЙЛЫ:
KIMI: AI_EXPERTS/EXPERTS/KIMI/output.md
GROK: AI_EXPERTS/EXPERTS/GROK/output.md
GPT: AI_EXPERTS/EXPERTS/GPT/output.md
GEMINI: AI_EXPERTS/EXPERTS/GEMINI/output.md
MASTER: AI_EXPERTS/MASTER_ANALYSIS_v3.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
Исправить критические баги P0:
1. API matching (db parameter)
2. Router import (HomeScreen)
3. Division by zero (scale_factor)
4. GeometryCalculator (stub values)
"""

# ================================================================================
# 📊 ТЕХНИЧЕСКОЕ СОСТОЯНИЕ
# ================================================================================

## Текущие возможности:
- Flutter app с Riverpod + GoRouter
- FastAPI backend с SQLite
- CV модули (contour, edge, geometry)
- Auto-alignment feature (ручное подтверждение)
- 23 unit теста проходят (но есть баги в API)

## Требуется срочно:
- Исправить API matching (падает)
- Исправить Router import (не запускается)
- Исправить GeometryCalculator (неверные данные)
- Обучить YOLO модель

# ================================================================================
# 📁 РАСПОЛОЖЕНИЕ КЛЮЧЕВЫХ ФАЙЛОВ
# =============================================================================

"""
📂 ОСНОВНОЙ ПУТЬ: /home/bot/porojects/ai_lock_project/

📋 ДЛЯ СТАРТА:
  📄 STARTUP.md - этот файл
  📄 OPENCODE_MASTER_PROMPT.txt - мастер промт для OpenCode

📊 ЭКСПЕРТЫ:
  📁 AI_EXPERTS/EXPERTS/KIMI/ - Архитектура
  📁 AI_EXPERTS/EXPERTS/GROK/ - Анализ кода
  📁 AI_EXPERTS/EXPERTS/GPT/ - Генерация кода
  📁 AI_EXPERTS/EXPERTS/GEMINI/ - ML/CV
  📁 AI_EXPERTS/MASTER_ANALYSIS_v3.md - Синтез

📁 ФАКТ (текущее состояние):
  📄 PROJECT_STATE.md
  📄 AI_EXPERTS/TECHNICAL_STATE.md
"""

# ================================================================================
# 📋 ЛОГ РАЗРАБОТКИ
# =============================================================================

"""
| Версия | Дата | Описание |
|--------|------|----------|
| 1.0.0 | 2026-02-22 | STARTUP создан |
| 3.0.4 | 2026-02-22 | P2 refactoring |
| 3.1.0 | 2026-02-22 | DIN mask fix |
| 4.0.0 | 2026-02-23 | Экспертиза v4 - критические баги |
"""

# ================================================================================
# КОНЕЦ STARTUP FILE
# ================================================================================
