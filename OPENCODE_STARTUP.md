# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Версия: 3.0.0 | Дата: 2026-02-22
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ:
1. STARTUP.md - стартовые инструкции
2. PROJECT_STATE.md - текущее состояние (обновлено)
3. OPENCODE_MASTER_PROMPT.txt - мастер промт

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (PostgreSQL/SQLite)
- cv_pipeline/ - Computer Vision (OpenCV + YOLO)
- datafordb/ - Данные для БД (181 замок)

## ТЕКУЩЕЕ СОСТОЯНИЕ:

### Оценки экспертов:
| Эксперт | Оценка |
|---------|--------|
| KIMI (Architecture) | 6.8/10 |
| GROK (Code Analysis) | 7.2/10 |
| GEMINI (ML/CV) | 6.0/10 |

### Компоненты:
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.0/10 | ✅ Готов |
| Backend | 7.2/10 | ✅ Готов |
| CV Pipeline | 6.0/10 | ⚠️ Нужен YOLO |
| Тесты | 23/23 | ✅ Проходят |

### Выполненные задачи:
1. ✅ PostgreSQL миграция (P0)
2. ✅ Flutter Catalog Screen (P1)
3. ✅ YOLO интеграция (структура)
4. ✅ База данных замков (147 замков)

## ПЛАН РАЗВИТИЯ

### P0 (Критический):
1. ~~PostgreSQL миграция~~ ✅
2. ~~База данных замков~~ ✅
3. YOLO датасет (500+ фото) - требует ручного сбора
4. Обучение YOLO

### P1 (Высокий):
5. ~~Flutter каталог~~ ✅
6. Camera integration - AR камера

### P2 (Средний):
7. Flutter widget тесты
8. Type hints
9. Документация

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### Маска отверстия под цилиндр:
- EURO_CYLINDER_HOLE = "33x17" mm

### Допуски:
- BACKSET_TOLERANCE = ±2.0 mm
- CENTER_DISTANCE_TOLERANCE = ±3.0 mm

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## ФАЙЛЫ ЭКСПЕРТОВ:
- KIMI: AI_EXPERTS/EXPERTS/KIMI/master_prompt.md
- GROK: AI_EXPERTS/EXPERTS/GROK/master_prompt.md
- GPT: AI_EXPERTS/EXPERTS/GPT/master_prompt.md
- GEMINI: AI_EXPERTS/EXPERTS/GEMINI/master_prompt.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
По KIMI - следующий приоритет Camera Integration (P1)

Проект: AI Lock Selector
Ветка: develop
Оценка: 6.8/10
"""

# ================================================================================
# END OF STARTUP PROMPT
# ================================================================================
