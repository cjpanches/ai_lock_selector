---
title: "AI_MASTER - Универсальный промпт для AI"
version: "1.0"
date_created: "2026-03-02"
status: "ACTIVE"
direction: "user_to_ai"
---

# AI Lock Selector - Полный контекст проекта

## Основная информация

| Параметр | Значение |
|----------|----------|
| Проект | AI Lock Selector |
| Версия | 4.5.0 |
| Директория | /home/bot/projects/ai_lock_project/ |

## Структура проекта

```
ai_lock_project/
├── mobile_app/          # Flutter + Riverpod + GoRouter
├── backend/             # FastAPI + SQLite (147 locks)
├── cv_pipeline/         # OpenCV + YOLO
├── AI_EXPERTS/         # Expert audits
├── mask/               # AR маска (euro_profile_exact.svg)
└── datafordb/          # 762 фото для YOLO
```

## Технологический стек

| Компонент | Технологии |
|-----------|------------|
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2, pytest |
| Mobile | Flutter 3.24+, Riverpod, GoRouter |
| CV | OpenCV 4.x, YOLOv8 OBB, NumPy |

## Текущее состояние

| Компонент | Статус |
|-----------|--------|
| Backend API | ✅ Работает (port 8001) |
| Flutter Web | ✅ Работает (port 8083) |
| Database | ✅ 147 замков |
| CV Pipeline | ⚠️ Частично |
| YOLO | ❌ Не обучен |

## Ключевые константы

### Euro Cylinder (калибровка)
```python
DIN_SLOT_WIDTH = 10.0      # mm - ЭТАЛОН
DIN_TOTAL_HEIGHT = 33.0   # mm
scale_factor = detected_pixels / 10.0
```

### YOLO классы
- 0: lock_plate (планка замка)
- 1: cylinder_hole (отверстие цилиндра 33x17mm)
- 2: handle_square (квадрат ручки 8x8mm)

### Точность измерений
- Target: ±0.5-1.0mm
- Center distance: ±3mm
- Backset: ±2mm
- Plate width: ±2mm
- Plate height: ±3mm

## База данных

- 147 замков (100% заполнено)
- Поля: backset, center_distance, plate_width, plate_height, body_width, body_height, square_hole_size

## Ссылки

- Status Dashboard: http://localhost:8080/ai_lock_project_status.html
- Prompt Hub: http://localhost:8081/
- Backend API: http://localhost:8001/docs
- Flutter Web: http://localhost:8083/

## Команды

```bash
# Запуск backend
cd /home/bot/projects/ai_lock_project/backend && pytest

# Тесты
cd /home/bot/projects/ai_lock_project/backend && pytest tests/ -v

# YOLO training
cd /home/bot/projects/ai_lock_project/cv_pipeline && python train_yolo.py --epochs 100
```

---

## ЗАДАЧА ДЛЯ AI

[ОПИШИ ЗДЕСЬ СВОЮ ЗАДАЧУ]

Примеры:
- "Проанализируй код и найди баги"
- "Создай новый компонент..."
- "Проведи аудит архитектуры"
- "Предложи улучшения производительности"
- "Исправь баг в файле X"
- "Напиши тесты для функции Y"

---

## Инструкции для AI

1. Используй технологии из стека проекта
2. Соблюдай конвенции кода:
   - Python: type hints, async/await, PEP 8
   - Dart: Equatable, Riverpod, camelCase
3. Пиши тесты для нового кода
4. Документируй сложные функции
5. Проверяй существование файлов перед изменением
6. Используй относительные пути от директории проекта
