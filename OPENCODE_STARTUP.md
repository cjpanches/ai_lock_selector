# ================================================================================
# 🚀 OPENCODE STARTUP PROMPT - AI LOCK SELECTOR
# ================================================================================
# Версия: 4.3.0 | Дата: 2026-02-28
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ:
1. STARTUP.md - стартовые инструкции
2. PROJECT_STATE.md - текущее состояние (v4.3.0)
3. AI_EXPERTS/MASTER_ANALYSIS_v3.md - мастер анализ

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite)
- cv_pipeline/ - Computer Vision (OpenCV + YOLO)
- AI_EXPERTS/ - Аудиты экспертов

## ТЕКУЩЕЕ СОСТОЯНИЕ (v4.3):

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
| Mobile App | 6.5/10 | ✅ Работает (кнопка фото исправлена) |
| Backend | 6.2/10 | ✅ Работает |
| CV Pipeline | 5.5/10 | ✅ Готов к пре-разметке |
| YOLO Dataset | 4.0/10 | ⚠️ Нужны фото |
| Tests | 6/10 | ✅ 38 тестов |

## ЧТО РАБОТАЕТ:
- ✅ Backend на localhost:8001 (147 замков)
- ✅ Flutter Web на localhost:8080
- ✅ AR Camera с DIN маской
- ✅ Кнопка фото (tap = normal, long press = force)
- ✅ API: /api/v1/locks, /api/v1/match, /api/v1/measure
- ✅ pre_label.py - пре-разметка для YOLO
- ✅ 38 unit тестов

## ЧТО НУЖНО СДЕЛАТЬ:
1. Собрать 500+ фото замков (правильный ракурс сверху)
2. Разметить в Roboflow
3. Обучить YOLO

## КЛЮЧЕВЫЕ ФАЙЛЫ:
- mobile_app/lib/providers/capture_provider.dart - кнопка фото
- mobile_app/lib/features/ar_camera/ar_camera_screen.dart - AR экран
- cv_pipeline/pre_label.py - пре-разметка
- cv_pipeline/train_yolo.py - обучение
- cv_pipeline/dataset/ - структура датасета

## ЗАПУСК:
Backend: cd backend && uvicorn app.main:app --port 8001
Flutter: cd mobile_app && flutter run

## ЭКСПЕРТЫ:
KIMI - Architecture
GROK - Code Analysis  
GPT - Code Generation
GEMINI - ML/CV
MASTER - Consensus
"""
