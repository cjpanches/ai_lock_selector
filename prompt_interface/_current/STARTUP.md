---
title: "STARTUP - Сессия разработки AI Lock Selector"
version: "1.0"
date_created: "2026-03-01"
status: "ACTIVE"
direction: "user_to_opencode"
---

# AI Lock Selector - Сессия разработки

## Текущее состояние проекта

| Компонент | Статус | Версия |
|-----------|--------|--------|
| Backend API | ✅ Работает | 8001 |
| Flutter Web | ✅ Работает | 8083 |
| Database | ✅ 147 замков | SQLite |
| CV Pipeline | ⚠️ Частично | v4.5 |
| YOLO | ❌ Не обучен | - |
| Tests | ✅ 38/38 | - |

## Версия проекта: 4.5.0

## Директория проекта
```
/home/bot/porojects/ai_lock_project/
```

## Основные задачи

1. **Аудит проекта** - проверка багов, конфликтов, связей
2. **Исправление критических багов**:
   - pre_label.py - hardcoded scale_factor
   - measurement_service.py - undefined variables
3. **Обучение YOLO** - 762 фото готовы
4. **Интеграция CV** - связать Flutter → Backend → YOLO

## Команды

```bash
# Запуск backend
cd /home/bot/porojects/ai_lock_project/backend && pytest

# Статус-дашборд
http://localhost:8080/ai_lock_project_status.html
```

## Последние исправления (v4.5.0)

- ✅ pre_label.py: убран hardcoded scale_factor, добавлена функция calculate_scale_from_marker()
- ✅ measurement_service.py: исправлен порядок вызовов, убраны hardcoded fallbacks
- ✅ 3 класса YOLO: lock_plate, cylinder_hole, handle_square

## Требования к точности

- Center distance: ±3mm
- Backset: ±2mm  
- Target: ±0.5-1.0mm

## Euro Cylinder (калибровка)

- Total height: 33mm
- Slot width: 10mm (эталон для калибровки)
- Formula: `scale_factor = detected_slot_pixels / 10.0`
