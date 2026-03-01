# Tasks for AI Agents

## Overview

Список задач, назначенных для AI агентов в рамках проекта AI Lock Selector.

## Priority Tasks

### Priority 1: Critical (Blocking)

| Task | Agent | Status | Description |
|------|-------|--------|-------------|
| YOLO Training | GEMINI | Pending | Train model on 762 photos |
| Scale Factor Fix | GEMINI | ✅ Done | Fix scale_factor calculation |
| Roboflow Setup | KIMI | Pending | Configure dataset and labels |

### Priority 2: High

| Task | Agent | Status | Description |
|------|-------|--------|-------------|
| PostgreSQL Migration | KIMI | Pending | Migrate from SQLite to PostgreSQL |
| Add Authentication | GROK | Pending | User auth system |
| Flutter Tests | GPT | Pending | Add widget tests |

### Priority 3: Medium

| Task | Agent | Status | Description |
|------|-------|--------|-------------|
| Rate Limiting | GROK | Pending | Add API rate limiting |
| Performance Optimization | GROK | Pending | Optimize CV pipeline |
| UI Improvements | GPT | Pending | Enhance AR overlay |

### Priority 4: Low

| Task | Agent | Status | Description |
|------|-------|--------|-------------|
| Documentation | KIMI | Ongoing | Keep docs updated |
| Error Messages | GROK | Pending | Improve error handling |

## Current Sprint Tasks

### Task 1: YOLO Model Training
```
Title: Train YOLO on 762 lock photos
Description: 
1. Upload photos to Roboflow
2. Create 3 classes: lock_plate, cylinder_hole, handle_square
3. Label all photos
4. Export YOLOv8 OBB
5. Train: python train_yolo.py --epochs 100

Assigned: GEMINI
Estimated: 4-8 hours (labeling) + 2-4 hours (training)
```

### Task 2: CV Pipeline Integration
```
Title: Integrate trained YOLO model
Description:
1. Update yolo_detector.py to use trained weights
2. Test end-to-end measurement accuracy
3. Verify ±0.5-1.0mm accuracy target

Assigned: GEMINI
Estimated: 2-4 hours
```

### Task 3: PostgreSQL Setup
```
Title: Set up PostgreSQL database
Description:
1. Create PostgreSQL instance
2. Migrate data from SQLite
3. Update connection string in config

Assigned: KIMI
Estimated: 2-3 hours
```

## Completed Tasks

| Task | Agent | Completed |
|------|-------|-----------|
| Scale Factor Bug Fix | GEMINI | v4.4 |
| Backend API Setup | KIMI | v1.0 |
| Flutter App Structure | GPT | v1.0 |
| Database Schema | KIMI | v1.0 |
| Basic CV Pipeline | GEMINI | v1.0 |

## Backlog

- Add user authentication
- Implement OAuth2
- Add push notifications
- Implement offline mode
- Add cloud sync
- Multi-language support (Russian, English)

## Related Documents

- [15_DEVELOPMENT_PLAN.md](./15_DEVELOPMENT_PLAN.md) - Full development plan
- [AGENTS.md](./AGENTS.md) - Agent instructions
- [COMPREHENSIVE_AUDIT_v4.4.md](./COMPREHENSIVE_AUDIT_v4.4.md) - Current status
