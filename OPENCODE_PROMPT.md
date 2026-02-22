# AI Lock Selector - System Audit & Continuation

## Current State (After Audit)

**Branch:** develop  
**Last Commit:** cfa57ec (Optimize Expert System Structure)
**GitHub:** https://github.com/cjpanches/ai_lock_selector
**Overall Score:** 5.2/10

---

## Project Overview

Mobile app for measuring door lock parameters via AR and finding analogs from company catalog.

---

## Structure

```
ai_lock_project/
├── mobile_app/          # Flutter app
│   ├── lib/
│   │   ├── core/
│   │   ├── domain/models/
│   │   ├── features/ar_camera/
│   │   └── main.dart
│   └── pubspec.yaml
│
├── backend/             # FastAPI
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── models/
│   └── requirements.txt
│
├── cv_pipeline/        # Computer Vision
│   └── src/
│       ├── contour_analyzer.py
│       ├── edge_detector.py
│       ├── geometry_calculator.py
│       └── lock_pipeline.py
│
└── AI_EXPERTS/         # Expert System
    ├── ORCHESTRATOR/
    ├── EXPERTS/
    │   ├── GROK/
    │   ├── KIMI/
    │   ├── GPT/
    │   ├── GEMINI/
    │   └── COPILOT/
    └── GENERAL_PLAN/
```

---

## Scores

| Component | Score |
|-----------|-------|
| Mobile App | 4.5/10 |
| Backend | 3.5/10 |
| CV Pipeline | 3.0/10 |
| Expert System | 8/10 |
| Documentation | 7/10 |
| **OVERALL** | **5.2/10** |

---

## Technical Debt (Priority Order)

### P0 - Critical
1. No Riverpod (plain setState) - Mobile
2. No navigation - Mobile
3. No PostgreSQL - Backend
4. No YOLO model - CV

### P1 - Important
5. No unit tests
6. No dataset collected

### P2 - Nice to have
7. No CI/CD

---

## What Needs to Be Done

### Priority 1: Backend & Database
- Connect PostgreSQL
- Create tables: locks, manufacturers, compatibility

### Priority 2: Flutter State Management
- Implement Riverpod
- Add navigation (go_router)
- Create 3 screens: Camera → Results → Catalog

### Priority 3: CV Pipeline
- Collect dataset (500+ images)
- Integrate YOLO model

### Priority 4: UI
- Add animations
- Improve DIN mask visual

---

## Key Constants

```dart
const double dinCylinderWidth = 10.0;   // mm
const double dinCylinderHeight = 17.0;  // mm
const double backsetTolerance = 2.0;
const double centerDistanceTolerance = 3.0;
```

---

## Commands

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Flutter
cd mobile_app && flutter run

# APK
cd mobile_app && flutter build apk --debug

# Python CV
cd cv_pipeline/src && python lock_pipeline.py
```

---

## Git Workflow

- Work in `develop` branch
- Commit changes
- Push to origin/develop

---

## Documentation

- `AGENTS.md` - AI agent instructions
- `CONTRIBUTING.md` - Developer guide
- `SYSTEM_AUDIT.md` - Latest audit results
- `AI_EXPERTS/` - Expert system prompts

---

## Expert System (AI_EXPERTS)

Use AI_EXPERTS/ for coordinated development:

1. **KIMI** - Define architecture for task
2. **GPT** - Generate code
3. **GEMINI** - Review ML/CV parts
4. **GROK** - Analyze code issues

Super prompts available in:
- `AI_EXPERTS/EXPERTS/GROK/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/KIMI/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/GPT/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/GEMINI/00_super_prompt.txt`
- `AI_EXPERTS/EXPERTS/COPILOT/00_super_prompt.txt`

---

## Next Recommended Task

Implement Riverpod state management in Flutter:
1. Add `flutter_riverpod` to pubspec.yaml
2. Create mask_position_provider.dart
3. Refactor ar_camera_screen.dart to use ConsumerWidget

See `SYSTEM_AUDIT.md` for full audit details.
