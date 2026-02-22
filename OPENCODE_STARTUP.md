# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Скопируйте этот промпт в OpenCode для начала работы
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
- GROK (Code Analysis): 7.0/10 - LSP ошибки в CV модулях
- GEMINI (ML/CV): 6.5/10 - Нет YOLO модели + Dataset
- KIMI: Синтез готов - Архитектура стабильна
- GPT: Рекомендации готовы - Недостаточно тестов

## ПРИОРИТЕТЫ:
1. P0: Собрать Dataset (500+ фото замков) + Обучить YOLO
2. P1: Исправить LSP ошибки в CV модулях
3. P2: Добавить тесты и документацию

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
APK: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter build apk --debug
Тесты Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter test
Тесты Backend: cd /home/bot/porojects/ai_lock_project/backend && pytest

## AI ЭКСПЕРТЫ - ВЫВОДЫ:
📄 AI_EXPERTS/EXPERTS/GROK/output.md - GROK анализ
📄 AI_EXPERTS/EXPERTS/GEMINI/output.md - GEMINI анализ  
📄 AI_EXPERTS/EXPERTS/KIMI/output.md - KIMI синтез
📄 AI_EXPERTS/EXPERTS/GPT/output.md - GPT рекомендации

## СЛЕДУЮЩАЯ ЗАДАЧА:
Выбери одно из направлений:
1. Собрать dataset для YOLO (500+ фото замков) - требует реальных фото
2. Исправить LSP ошибки в CV модулях (cv2, numpy импорты)
3. Добавить больше unit тестов

Проект: AI Lock Selector
Ветка: develop
Оценка: 7.0/10
"""

# ================================================================================
# END OF STARTUP PROMPT
# ================================================================================
