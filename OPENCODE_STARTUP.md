# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Версия: 3.0.0 | Дата: 2026-02-22
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ:
1. STARTUP.md - стартовые инструкции
2. AI_EXPERTS/FACT/current_architecture_state.txt - текущее состояние
3. AI_EXPERTS/IDEAL/target_architecture.txt - целевое состояние

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite, порт 8000)
- cv_pipeline/src/ - Computer Vision (OpenCV)
- AI_EXPERTS/ - Экспертная система

## ТЕКУЩЕЕ СОСТОЯНИЕ (независимая экспертиза):

### Оценки экспертов:
| Эксперт | Оценка |
|---------|--------|
| KIMI (Architecture) | 6.8/10 |
| GROK (Code Analysis) | 7.2/10 |
| GEMINI (ML/CV) | 6.0/10 |

### Компоненты:
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.0/10 | Готов |
| Backend | 7.2/10 | Готов |
| CV Pipeline | 6.0/10 | Требует YOLO |
| Тесты | 23/23 | ✅ Проходят |

### Главные проблемы:
1. Нет YOLO модели (критический)
2. Нет датасета (500+ фото)
3. SQLite не для production
4. Flutter каталог не реализован

## ПЛАН РАЗВИТИЯ

### P0 (Критический):
1. Сбор датасета (500+ фото замков)
2. Обучение YOLO модели
3. Интеграция YOLO в lock_pipeline

### P1 (Высокий):
4. PostgreSQL миграция
5. Flutter каталог замков
6. Интеграция камеры

### P2 (Средний):
7. Flutter widget тесты
8. Type hints
9. Документация

## ТРЕБОВАНИЯ:
- Точность CV: ±1.5mm
- API response: < 200ms
- Покрытие тестами: > 70%

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## ФАЙЛЫ ЭКСПЕРТОВ:
- KIMI: AI_EXPERTS/EXPERTS/KIMI/analysis_result.md
- GROK: AI_EXPERTS/EXPERTS/GROK/analysis_result.md
- GPT: AI_EXPERTS/EXPERTS/GPT/analysis_result.md
- GEMINI: AI_EXPERTS/EXPERTS/GEMINI/analysis_result.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
Определи приоритет: YOLO датасет, PostgreSQL миграция, или Flutter каталог

Проект: AI Lock Selector
Ветка: develop
Оценка: 6.8/10
"""

# ================================================================================
# END OF STARTUP PROMPT
# ================================================================================
