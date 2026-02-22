# ================================================================================
# AI LOCK SELECTOR - STARTUP FILE
# ================================================================================
# Версия: 3.0.0
# Дата: 2026-02-22
# Проект: AI Lock Selector
# Репозиторий: https://github.com/cjpanches/ai_lock_selector
# Ветка: develop
# Оценка: 6.8/10
# ================================================================================

# ================================================================================
# 🚀 STARTUP PROMPT - СКОПИРУЙТЕ В OPENCODE
# ================================================================================

"""
Изучи проект AI Lock Selector в /home/bot/porojects/ai_lock_project/

## ОСНОВНЫЕ ФАЙЛЫ (в порядке приоритета):
1. STARTUP.md - этот файл (стартовые инструкции)
2. OPENCODE_STARTUP.md - промт для OpenCode (то же содержимое)
3. AI_EXPERTS/FACT/current_architecture_state.txt - текущее состояние
4. AI_EXPERTS/IDEAL/target_architecture.txt - целевое состояние

## СТРУКТУРА ПРОЕКТА:
- mobile_app/ - Flutter приложение (Riverpod + GoRouter)
- backend/ - FastAPI сервер (SQLite, порт 8000)
- cv_pipeline/src/ - Computer Vision (OpenCV)
- AI_EXPERTS/ - Экспертная система

## ТЕКУЩЕЕ СОСТОЯНИЕ (независимая экспертиза):
| Компонент | Оценка | Статус |
|-----------|--------|--------|
| Mobile App | 7.0/10 | Готов |
| Backend | 7.2/10 | Готов |
| CV Pipeline | 6.0/10 | Требует YOLO |
| Тесты | 23/23 | ✅ Проходят |

## РЕЗУЛЬТАТЫ ЭКСПЕРТОВ:
- KIMI (Architecture): 6.8/10 - Архитектура в порядке
- GROK (Code Analysis): 7.2/10 - Качество хорошее
- GPT (Code Generation): - Код сгенерирован
- GEMINI (ML/CV): 6.0/10 - Требует YOLO модель

## ПРИОРИТЕТЫ:
1. P0: Собрать Dataset (500+ фото) + Обучить YOLO
2. P1: PostgreSQL миграция
3. P1: Flutter каталог + интеграция камеры
4. P2: Тесты и документация

## ГЛАВНЫЕ РИСКИ:
- Нет YOLO модели (критический)
- Нет датасета (требует ручной работы)
- SQLite не для production

## КОМАНДЫ ЗАПУСКА:
Backend: cd /home/bot/porojects/ai_lock_project/backend && PYTHONPATH=. uvicorn app.main:app --reload
Flutter: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter run
APK: cd /home/bot/porojects/ai_lock_project/mobile_app && flutter build apk --debug
Тесты: cd /home/bot/porojects/ai_lock_project/backend && pytest

## AI ЭКСПЕРТЫ - ФАЙЛЫ:
KIMI: AI_EXPERTS/EXPERTS/KIMI/analysis_result.md
GROK: AI_EXPERTS/EXPERTS/GROK/analysis_result.md  
GPT: AI_EXPERTS/EXPERTS/GPT/analysis_result.md
GEMINI: AI_EXPERTS/EXPERTS/GEMINI/analysis_result.md

## СЛЕДУЮЩАЯ ЗАДАЧА:
Определить приоритет: YOLO датасет или PostgreSQL миграция
"""

# ================================================================================
# 📊 ТЕХНИЧЕСКОЕ СОСТОЯНИЕ
# ================================================================================

## Текущие возможности:
- Flutter app с Riverpod + GoRouter
- FastAPI backend с SQLite
- CV модули (contour, edge, geometry)
- 23 unit теста проходят

## Требуется доработка:
- YOLO модель (нет обученной)
- Датасет 500+ фото
- PostgreSQL для production
- Flutter каталог замков

# ================================================================================
# 📁 РАСПОЛОЖЕНИЕ КЛЮЧЕВЫХ ФАЙЛОВ
# ================================================================================

"""
📂 ОСНОВНОЙ ПУТЬ: /home/bot/porojects/ai_lock_project/

📋 ДЛЯ СТАРТА:
  📄 STARTUP.md - этот файл
  📄 OPENCODE_STARTUP.md - промт для OpenCode

📊 ЭКСПЕРТЫ:
  📁 AI_EXPERTS/EXPERTS/KIMI/ - Архитектура
  📁 AI_EXPERTS/EXPERTS/GROK/ - Анализ кода
  📁 AI_EXPERTS/EXPERTS/GPT/ - Генерация кода
  📁 AI_EXPERTS/EXPERTS/GEMINI/ - ML/CV

📁 ФАКТ (текущее состояние):
  📄 AI_EXPERTS/FACT/current_architecture_state.txt

📁 IDEAL (целевое состояние):
  📄 AI_EXPERTS/IDEAL/target_architecture.txt
"""

# ================================================================================
# 📋 ЛОГ РАЗРАБОТКИ
# ================================================================================

"""
| Версия | Дата | Описание |
|--------|------|----------|
| 1.0.0 | 2026-02-22 | STARTUP создан |
| 2.0.0 | 2026-02-22 | Первая версия |
| 2.1.0 | 2026-02-22 | После экспертизы v1 |
| 3.0.0 | 2026-02-22 | Независимая экспертиза |
"""

# ================================================================================
# КОНЕЦ STARTUP FILE
# ================================================================================
