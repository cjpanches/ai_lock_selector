# ================================================================================
# AI LOCK SELECTOR - STARTUP FILE
# ================================================================================
# Версия: 3.0.4
# Дата: 2026-02-22
# Проект: AI Lock Selector
# Репозиторий: https://github.com/cjpanches/ai_lock_selector
# Ветка: develop
# Оценка: 7.5/10
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

## ТЕКУЩЕЕ СОСТОЯНИЕ (v3.0.4):
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.8/10 | ✅ Готов |
| Backend | 7.2/10 | ✅ Готов |
| CV Pipeline | 6.0/10 | ⚠️ Нужен YOLO |
| Auto-Alignment | 7.5/10 | ✅ Готов |
| Тесты | 23/23 | ✅ Проходят |
| **Общая** | **7.5/10** | ✅ |

## ВЫПОЛНЕННЫЕ ЗАДАЧИ:
1. ✅ PostgreSQL миграция
2. ✅ Flutter Catalog Screen
3. ✅ YOLO интеграция (структура)
4. ✅ Auto-alignment с CV
5. ✅ P0 баги исправлены
6. ✅ P1: retry + confidence
7. ✅ P2: SRP refactoring + Equatable

## ПРИОРИТЕТЫ:
1. P3: Собрать Dataset (500+ фото) + Обучить YOLO
2. P3: PostgreSQL в production
3. P4: Документация

## ГЛАВНЫЕ РИСКИ:
- Нет YOLO модели (требует ручной сбор фото)
- SQLite не для production

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
APK: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter build apk --debug
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## AI ЭКСПЕРТЫ - ФАЙЛЫ:
KIMI: AI_EXPERTS/EXPERTS/KIMI/analysis_result_v3.md
GROK: AI_EXPERTS/EXPERTS/GROK/analysis_result_v3.md
GPT: AI_EXPERTS/EXPERTS/GPT/analysis_result_v3.md
GEMINI: AI_EXPERTS/EXPERTS/GEMINI/analysis_result_v3.md
MASTER: AI_EXPERTS/MASTER_ANALYSIS_v3.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
YOLO Dataset collection (ручная работа - 500+ фото замков)
"""

# ================================================================================
# 📊 ТЕХНИЧЕСКОЕ СОСТОЯНИЕ
# ================================================================================

## Текущие возможности:
- Flutter app с Riverpod + GoRouter
- FastAPI backend с SQLite
- CV модули (contour, edge, geometry)
- Auto-alignment feature
- 23 unit теста проходят
- SRP refactoring выполнен
- Equatable добавлен

## Требуется доработка:
- YOLO модель (нет обученной)
- Датасет 500+ фото
- PostgreSQL для production

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
| 2.0.0 | 2026-02-22 | Первая версия |
| 2.1.0 | 2026-02-22 | После экспертизы v1 |
| 3.0.0 | 2026-02-22 | Независимая экспертиза |
| 3.0.2 | 2026-02-22 | P0 баги исправлены |
| 3.0.3 | 2026-02-22 | P1 улучшения |
| 3.0.4 | 2026-02-22 | P2 refactoring |
"""

# ================================================================================
# КОНЕЦ STARTUP FILE
# ================================================================================
