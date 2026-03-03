# ================================================================================
# 🚀 OPENCODE STARTUP - PROJECT MANAGER
# ================================================================================
# Version: 5.0.0 | Date: 2026-03-03
# ================================================================================

## PORT MONITORING

| Порт | Проект | Статус | Ссылка |
|------|--------|--------|--------|
| 8080 | Project Manager | ✅ Работает | http://localhost:8080/ |
| 8081 | Prompt Hub | ✅ Работает | http://localhost:8081/prompt_dashboard.html |
| 8082 | AI Lock Status | ✅ Работает | http://localhost:8082/ |
| 8083 | Voice Secretary | По требованию | http://localhost:8083/ |
| 8084 | Flutter Web | По требованию | cd mobile_app && flutter build web |

## QUICK START

```bash
# Project Manager
http://localhost:8080/

# AI Lock Selector Status
http://localhost:8082/

# Prompt Hub
http://localhost:8081/prompt_dashboard.html

# Voice Secretary (требует запуска)
cd /home/bot/projects/assistant-project/v2
```

## PROJECT STRUCTURE

```
/home/bot/projects/
├── PROJECT_MANAGER/           # Система управления
│   ├── PROJECT_MANAGER.md     # Этот файл
│   ├── dashboard.html         # Главный дашборд
│   └── pages/               # Страницы проектов
├── ai_lock_project/          # AI Lock Selector
│   ├── mobile_app/          # Flutter приложение
│   ├── backend/             # FastAPI
│   ├── cv_pipeline/         # YOLO
│   └── prompt_interface/    # Prompt Hub
└── assistant-project/       # Voice Secretary
    └── v2/                  # Основная версия
```

## PROJECTS

### 1. AI Lock Selector (🔒)
- **Описание:** Мобильное приложение для измерения дверных замков через AR
- **Статус:** Активен
- **Ссылка:** http://localhost:8082/
- **Компоненты:**
  - Backend API (port 8001)
  - Flutter Web (port 8084, по требованию)
  - Database: 147 замков
  - YOLO: Не обучен

### 2. Prompt Hub (📋)
- **Описание:** Система управления мастер-промптами
- **Статус:** Активен
- **Ссылка:** http://localhost:8081/prompt_dashboard.html
- **Промпты:**
  - AI_MASTER - Универсальный для AI
  - STARTUP - Контекст проекта
  - AUDIT - Шаблон аудита
  - FIX_BUG - Шаблон бага

### 3. Voice Secretary (🎤)
- **Описание:** Голосовой секретарь с AI анализом
- **Статус:** Готов (требует запуска)
- **Ссылка:** http://localhost:8083/
- **Требования:**
  - Flask сервер
  - Whisper (транскрипция)
  - Ollama (AI анализ)

## COMMANDS

```bash
# Запуск Project Manager
cd /home/bot/projects/PROJECT_MANAGER
python3 -m http.server 8080

# Запуск Prompt Hub
cd /home/bot/projects/ai_lock_project/prompt_interface
python3 -m http.server 8081

# Запуск AI Lock Status
cd /home/bot/projects
python3 -m http.server 8082

# Запуск Voice Secretary
cd /home/bot/projects/assistant-project/v2
source ../myenv/bin/activate
python app.py

# Flutter Web (по требованию)
cd /home/bot/projects/ai_lock_project/mobile_app
flutter build web
python3 -m http.server 8084 -d build/web/
```

## AI EXCHANGE

Для работы с внешними AI используй Prompt Hub (порт 8081):
- Копирование промптов
- Сохранение ответов от AI
- Интеграция с Voice Secretary

## KEY MEASUREMENTS (AI Lock)

- Center Distance: 50-92mm (±3mm)
- Backset: 20-68mm (±2mm)
- Euro Cylinder: 33mm height, 10mm slot width (calibration)

## DATABASE

- 147 замков (100% заполнено)
- Поля: backset, center_distance, plate_width, plate_height, body_width, body_height, square_hole_size

================================================================================
END OF STARTUP
================================================================================
