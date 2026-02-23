# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Версия: 4.0.0 | Дата: 2026-02-23
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ:
1. STARTUP.md - стартовые инструкции
2. PROJECT_STATE.md - текущее состояние (v4.0.0)
3. OPENCODE_MASTER_PROMPT.txt - мастер промт

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (PostgreSQL/SQLite)
- cv_pipeline/ - Computer Vision (OpenCV + YOLO)
- datafordb/ - Данные для БД (147 замков)

## ТЕКУЩЕЕ СОСТОЯНИЕ:

### Оценки экспертов (v4.0):
| Эксперт | Оценка |
|---------|--------|
| KIMI (Architecture) | 5.5/10 |
| GROK (Code Analysis) | 5.8/10 |
| GEMINI (ML/CV) | 4/10 |
| GPT (Code Generation) | 5.5/10 |
| **MASTER** | **5.2/10** |

### Компоненты:
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 6.1/10 | ⚠️ Router import missing |
| Backend | 5.4/10 | 🔴 API crash |
| CV Pipeline | 5.4/10 | 🔴 Broken |
| Tests | 3/10 | ❌ Low |

## КРИТИЧЕСКИЕ БАГИ (P0):

1. 🔴 API matching crash - missing `db` parameter
   - backend/app/api/matching.py:14
   - backend/app/api/measurements.py:38

2. 🔴 Router import missing - HomeScreen not imported
   - mobile_app/lib/core/router.dart:3

3. 🔴 Division by zero - scale_factor validation missing
   - cv_pipeline/src/lock_pipeline.py:136

4. 🔴 GeometryCalculator broken - stub values
   - cv_pipeline/src/geometry_calculator.py:54 (returns 3.0)
   - cv_pipeline/src/geometry_calculator.py:158 (center_distance = backset)

## ПЛАН РАЗВИТИЯ

### P0 (Критический - Немедленно):
1. Исправить API matching (добавить db parameter)
2. Исправить Router import (добавить HomeScreen)
3. Исправить division by zero (scale_factor validation)
4. Исправить GeometryCalculator (реализовать расчёт)

### P1 (Высокий - Следующий спринт):
5. Исправить CORS security
6. Убрать mock данные из measurement_service
7. Добавить тесты

### P2 (Средний - Квартал):
8. Обучить YOLO модель (500+ фото)
9. Рефакторинг кода
10. Улучшить архитектуру

## КЛЮЧЕВЫЕ КОНСТАНТЫ

### Маска отверстия под цилиндр:
- EURO_CYLINDER_HOLE = "33x17" mm (DIN)

### Допуски (требуют улучшения):
- BACKSET_TOLERANCE = ±2.0 mm (цель: ±1.5mm)
- CENTER_DISTANCE_TOLERANCE = ±3.0 mm (цель: ±1.5mm)

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## ФАЙЛЫ ЭКСПЕРТОВ:
- KIMI: AI_EXPERTS/EXPERTS/KIMI/output.md
- GROK: AI_EXPERTS/EXPERTS/GROK/output.md
- GPT: AI_EXPERTS/EXPERTS/GPT/output.md
- GEMINI: AI_EXPERTS/EXPERTS/GEMINI/output.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
Исправить критические баги P0 (API matching, Router import)

Проект: AI Lock Selector
Ветка: develop
Оценка: 5.2/10 (требует критических исправлений)
"""

# ================================================================================
# END OF STARTUP PROMPT
# ================================================================================
