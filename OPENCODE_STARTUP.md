# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Версия: 4.4.0 | Дата: 2026-02-28
# =============================================================================

## ОСНОВНЫЕ ФАЙЛЫ:
1. STARTUP.md - стартовые инструкции
2. COMPREHENSIVE_AUDIT_v4.4.md - полный аудит (НОВЫЙ!)
3. OPENCODE_STARTUP.md - этот файл
4. ROBOFLOW_INSTRUCTION.md - инструкция для Roboflow

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite, 147 замков)
- cv_pipeline/ - Computer Vision (OpenCV + YOLO)
- AI_EXPERTS/ - Аудиты экспертов
- mask/ - AR маска (euro_profile_exact.svg - ИСТОЧНИК ИСТИНЫ)
- photo for aducation/ - 934 фото собрано

## ТЕКУЩЕЕ СОСТОЯНИЕ (v4.4):

### Оценки экспертов:
| Эксперт | Оценка |
|---------|--------|
| KIMI (Architecture) | 5.8/10 |
| GROK (Code Analysis) | 5.8/10 |
| GPT (Code Generation) | 5.5/10 |
| GEMINI (ML/CV) | 5.5/10 |
| **MASTER** | **5.6/10** |

### Компоненты:
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 6.5/10 | ✅ Работает |
| Backend | 6.2/10 | ✅ Работает (port 8001) |
| CV Pipeline | 6.0/10 | ✅ Исправлен баг калибровки |
| YOLO Dataset | 5.0/10 | ⚠️ 934 фото, нужна разметка |
| Tests | 6/10 | ✅ 38/38 тестов |

## ЧТО РАБОТАЕТ:
- ✅ Backend на localhost:8001 (147 замков)
- ✅ Flutter Web на localhost:8083
- ✅ AR Camera с DIN маской (правильная геометрия!)
- ✅ API: /api/v1/locks, /api/v1/match, /api/v1/measure
- ✅ 38 unit тестов (все проходят)
- ✅ 934 фото собрано

## КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ (v4.4):

### Баг калибровки scale_factor ИСПРАВЛЕН!
- **Было:** max(w,h) / 10.0 → 33mm вместо 10mm (ОШИБКА 230%!)
- **Стало:** min(w,h) / 10.0 → правильная ширина слота 10mm

### Файлы изменены:
- cv_pipeline/src/lock_pipeline.py
- cv_pipeline/src/geometry_calculator.py  
- cv_pipeline/train_yolo.py
- cv_pipeline/dataset/lock_dataset.yaml

## ЧТО НУЖНО СДЕЛАТЬ:
1. Обработать 934 фото (извлечь из видео или использовать IMG_*)
2. Загрузить в Roboflow
3. Разметить 4 класса (lock_plate, cylinder_hole, mounting_hole, handle_square)
4. Обучить YOLO: python train_yolo.py --epochs 100

## РАЗМЕРЫ ЕВРОЦИЛИНДРА (ЭТАЛОН!):
```
Total height: 33mm
Top circle: 17mm diameter
Slot width: 10mm ← ЭТО ДЛЯ КАЛИБРОВКИ
Bottom semicircle: 10mm diameter

pixels_per_mm = detected_slot_width_pixels / 10.0
```

## КЛЮЧЕВЫЕ ФАЙЛЫ:
- mask/euro_profile_exact.svg - точные размеры цилиндра (ИСТОЧНИК ИСТИНЫ)
- cv_pipeline/src/lock_pipeline.py - CV пайплайн (ИСПРАВЛЕН)
- cv_pipeline/src/geometry_calculator.py - расчёты размеров
- cv_pipeline/train_yolo.py - обучение YOLO
- ROBOFLOW_INSTRUCTION.md - инструкция по разметке

## ЗАПУСК:
Backend: cd backend && uvicorn app.main:app --port 8001
Flutter: cd mobile_app && flutter run
Тесты: cd backend && pytest

## ЭКСПЕРТЫ:
KIMI - Architecture
GROK - Code Analysis  
GPT - Code Generation
GEMINI - ML/CV
MASTER - Consensus

## ВАЖНО!
Класс cylinder_hole (ID=1) - самый важный:
- Это объект для детекции YOLO
- Это также эталон масштаба для калибровки
- 10mm слот - для расчёта pixels_per_mm
