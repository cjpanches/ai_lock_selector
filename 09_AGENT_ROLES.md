# Agent Roles

## Overview

Проект использует multiple AI агентов для различных задач анализа и разработки. Каждый агент специализируется в своей области.

## AI Agents

### 1. KIMI (Architecture Expert)

**Role:** System Architecture and Planning

**Strengths:**
- System architecture design
- Technology stack decisions
- Project planning
- Database schema design
- API design patterns

**Files Analyzed:**
- `backend/app/main.py`
- `backend/app/db/models.py`
- `AGENTS.md`

**Score:** 5.8/10

---

### 2. GEMINI (ML/CV Expert)

**Role:** Computer Vision and Machine Learning

**Strengths:**
- YOLO model configuration
- OpenCV algorithms
- Image processing
- Scale calibration
- Geometry calculations

**Files Analyzed:**
- `cv_pipeline/src/lock_pipeline.py`
- `cv_pipeline/src/geometry_calculator.py`
- `cv_pipeline/train_yolo.py`

**Critical Fix:** Identified and fixed scale_factor bug (using min() instead of max())

**Score:** 5.5/10

---

### 3. GROK (Code Analysis Expert)

**Role:** Code Quality and Best Practices

**Strengths:**
- Code structure analysis
- Error detection
- Performance optimization
- Security review
- Type safety

**Files Analyzed:**
- All Python files in backend/
- All Python files in cv_pipeline/

**Recommendations:**
- Fix LSP errors
- Add Pydantic validation
- Add rate limiting

**Score:** 5.8/10

---

### 4. GPT (Code Generation Expert)

**Role:** Code Generation and Flutter

**Strengths:**
- Flutter/Dart development
- Riverpod state management
- UI/UX implementation
- API integration

**Files Analyzed:**
- `mobile_app/lib/` - All Dart files
- `AGENTS.md`

**Recommendations:**
- Extract common widgets
- Add Flutter widget tests

**Score:** 5.5/10

---

## Collaboration Model

```
┌─────────────┐
│   Project   │
│   Context   │
└──────┬──────┘
       │
       ▼
┌─────────────┬─────────────┬─────────────┐
│    KIMI     │   GEMINI    │    GROK    │
│  (Arch)     │   (ML/CV)   │  (Code)    │
└──────┬──────┴──────┬──────┴──────┬──────┘
       │             │             │
       ▼             ▼             ▼
  Architecture   CV Pipeline   Code Quality
  Decisions      Models        Improvements
       │             │             │
       └─────────────┴─────────────┘
                     │
                     ▼
              Implementation
                     │
                     ▼
              ┌─────────────┐
              │     GPT    │
              │ (Flutter)  │
              └─────────────┘
```

## Expert Reviews

All expert reviews are documented in:
- `EXPERT_REVIEWS.txt` - Summary of all reviews
- `COMPREHENSIVE_AUDIT_v4.4.md` - Full audit report
- `AI_EXPERTS/` - Individual expert analysis files

## Workflow

1. **Initial Analysis**: KIMI provides architecture overview
2. **Technical Review**: GEMINI reviews CV/ML components
3. **Code Quality**: GROK analyzes code structure
4. **Implementation**: GPT generates Flutter code
5. **Consolidation**: All reviews merged into audit

## Related Documents

- [AI_EXPERTS/](./AI_EXPERTS/) - Expert analysis files
- [COMPREHENSIVE_AUDIT_v4.4.md](./COMPREHENSIVE_AUDIT_v4.4.md) - Full audit
- [EXPERT_REVIEWS.txt](./EXPERT_REVIEWS.txt) - Expert summary
