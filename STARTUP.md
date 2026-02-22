# ================================================================================
# AI LOCK SELECTOR - STARTUP FILE
# ================================================================================
# Версия: 2.1.0
# Дата: 2026-02-22
# Проект: AI Lock Selector
# Репозиторий: https://github.com/cjpanches/ai_lock_selector
# Ветка: develop
# Оценка: 7.0/10
# ================================================================================

# ================================================================================
# 🚀 STARTUP PROMPT - СКОПИРУЙТЕ В OPENCODE
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ (в порядке приоритета):
1. STARTUP.md - этот файл (стартовые инструкции)
2. OPENCODE_STARTUP.md - промпт для OpenCode (то же содержимое)
3. AI_EXPERTS/TECHNICAL_STATE.md - техническое состояние
4. AI_EXPERTS/EXPERT_INSTRUCTIONS.md - инструкции для экспертов
5. PROJECT_STATE.md - состояние проекта
6. SYSTEM_AUDIT.md - аудит

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite, порт 8000)
- cv_pipeline/src/ - Computer Vision (YOLO + OpenCV)
- AI_EXPERTS/ - Экспертная система

## ТЕКУЩЕЕ СОСТОЯНИЕ (после экспертизы):
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.5/10 | Готов |
| Backend | 7.0/10 | Готов |
| CV Pipeline | 6.0/10 | Требует YOLO модель |
| DevOps | 8.0/10 | Готов |

## РЕЗУЛЬТАТЫ ЭКСПЕРТОВ:
- GROK (Code Analysis): 7.0/10 - LSP ошибки
- GEMINI (ML/CV): 6.5/10 - Нет YOLO модели
- KIMI: Синтез готов
- GPT: Рекомендации готовы

## ПРИОРИТЕТЫ:
1. P0: Собрать Dataset + Обучить YOLO
2. P1: Исправить LSP ошибки
3. P2: Добавить тесты

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
APK: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter build apk --debug
Тесты: cd mobile_app && flutter test / cd backend && pytest

## AI ЭКСПЕРТЫ:
ВЫВОДЫ ЭКСПЕРТОВ В:
- AI_EXPERTS/EXPERTS/GROK/output.md
- AI_EXPERTS/EXPERTS/GEMINI/output.md
- AI_EXPERTS/EXPERTS/KIMI/output.md
- AI_EXPERTS/EXPERTS/GPT/output.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
Собрать dataset для YOLO (500+ фото замков) или исправить LSP ошибки в CV модулях.
"""

# ================================================================================
# 📁 РАСПОЛОЖЕНИЕ КЛЮЧЕВЫХ ФАЙЛОВ
# ================================================================================

"""
📂 ОСНОВНОЙ ПУТЬ: /home/bot/porojects/ai_lock_project/

📋 ДЛЯ СТАРТА:
  📄 OPENCODE_STARTUP.md - промпт для OpenCode (СКОПИРОВАТЬ!)
  📄 STARTUP.md - этот файл

📊 ТЕХНИЧЕСКОЕ СОСТОЯНИЕ:
  📄 AI_EXPERTS/TECHNICAL_STATE.md - полное состояние проекта
  📄 AI_EXPERTS/EXPERT_INSTRUCTIONS.md - инструкции для экспертов
  📄 AI_EXPERTS/EXPERT_OUTPUT_TEMPLATE.md - шаблон вывода

📝 РЕЗУЛЬТАТЫ ЭКСПЕРТОВ:
  📄 AI_EXPERTS/EXPERTS/GROK/output.md
  📄 AI_EXPERTS/EXPERTS/GEMINI/output.md
  📄 AI_EXPERTS/EXPERTS/KIMI/output.md
  📄 AI_EXPERTS/EXPERTS/GPT/output.md

📁 ИСХОДНЫЙ КОД:
  📁 mobile_app/lib/ - Flutter приложение
  📁 backend/app/ - FastAPI сервер
  📁 cv_pipeline/src/ - CV модули
"""

# ================================================================================
# 📊 ЛОГ РАЗРАБОТКИ
# ================================================================================

"""
| Версия | Дата | Описание |
|--------|------|----------|
| 1.0.0 | 2026-02-22 | STARTUP файл создан |
| 1.0.7 | 2026-02-22 | CI/CD, UI, Тесты |
| 2.0.0 | 2026-02-22 | Первая версия завершена |
| 2.1.0 | 2026-02-22 | После экспертизы |
"""

# ================================================================================
# КОНЕЦ STARTUP FILE
# ================================================================================
