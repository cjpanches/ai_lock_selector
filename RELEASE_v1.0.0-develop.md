# AI Lock Selector - Release v1.0.0-develop

## Дата: 2026-02-22

## Changes (Auto-alignment)
- Add auto-alignment button to AR camera screen
- Auto-detect lock position via CV backend  
- Enhanced mask_provider with auto-detection support

## Build
- Debug APK: `mobile_app/build/app/outputs/flutter-apk/app-debug.apk`
- Size: ~101 MB

## Project Status
| Component | Status |
|-----------|--------|
| Backend | ✅ Ready (FastAPI + PostgreSQL/SQLite) |
| Mobile | ✅ Ready (Flutter + Riverpod) |
| CV Pipeline | ⚠️ Needs YOLO training data |
| Tests | ✅ 23/23 passed |

## Download APK
[Download from GitHub Releases](#)

## Следующие шаги
1. Собрать YOLO датасет (500+ фото)
2. Обучить YOLO модель
3. Добавить widget тесты для Flutter
