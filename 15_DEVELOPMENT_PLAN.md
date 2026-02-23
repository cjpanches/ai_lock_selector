# DEVELOPMENT PLAN - AI Lock Selector
# ======================================
# Version: 4.0.0
# Date: 2026-02-23
# Based on: KIMI Architecture Analysis
# ======================================

---

## VISION

Создать мобильное приложение для точного измерения параметров дверных замков через AR камеру с подбором аналогов из каталога.

**Целевая точность:** ±1.5mm

---

## CURRENT STATUS (v4.0.0)

### Scores:
- Overall: 5.2/10 🔴
- Mobile App: 6.1/10 ⚠️
- Backend: 5.4/10 🔴
- CV Pipeline: 5.4/10 🔴
- Tests: 3/10 ❌

### Critical Issues (P0):
1. API matching crash (missing db parameter)
2. Router import missing
3. Division by zero in CV
4. GeometryCalculator broken (stub values)

---

## ROADMAP

### PHASE 1: CRITICAL FIXES (Week 1-2)
**Goal:** Make project runnable

#### P0 - Must Fix:
- [ ] Fix API matching (db parameter) - backend/app/api/matching.py:14
- [ ] Fix API matching - backend/app/api/measurements.py:38
- [ ] Fix Router import - mobile_app/lib/core/router.dart:3
- [ ] Fix division by zero - cv_pipeline/src/lock_pipeline.py:136
- [ ] Fix GeometryCalculator - cv_pipeline/src/geometry_calculator.py

#### P1 - Should Fix:
- [ ] Fix CORS security - backend/app/main.py:24
- [ ] Remove mock data from measurement_service
- [ ] Add basic tests

**Deliverable:** Working MVP with manual alignment

---

### PHASE 2: STABILIZATION (Week 3-4)
**Goal:** Reliable basic functionality

#### Backend:
- [ ] Add input validation
- [ ] Add error handling
- [ ] Add logging
- [ ] Fix test coverage to 50%+

#### Mobile:
- [ ] Add error boundaries
- [ ] Improve error messages
- [ ] Add loading states

#### CV:
- [ ] Add scale_factor validation
- [ ] Fix tolerance values (target: ±1.5mm)
- [ ] Add confidence scores

**Deliverable:** Stable MVP with 50% test coverage

---

### PHASE 3: FEATURES (Week 5-8)
**Goal:** Production-ready features

#### CV Pipeline:
- [ ] Implement auto-alignment
- [ ] Train YOLO model (500+ images)
- [ ] Add automatic measurements
- [ ] Achieve ±1.5mm accuracy

#### Backend:
- [ ] PostgreSQL in production
- [ ] Add caching (Redis)
- [ ] Add rate limiting
- [ ] Add monitoring

#### Mobile:
- [ ] Add measurement capture flow
- [ ] Improve UI/UX
- [ ] Add animations

**Deliverable:** Production-ready application

---

### PHASE 4: OPTIMIZATION (Week 9-12)
**Goal:** Scale and improve

- [ ] YOLO model optimization
- [ ] Performance optimization
- [ ] Horizontal scaling
- [ ] Advanced analytics

---

## DETAILED TASKS

### Backend Tasks
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Fix API matching | P0 | 1hr | Backend |
| Fix CORS | P1 | 1hr | Backend |
| Add validation | P1 | 2hr | Backend |
| Add logging | P1 | 1hr | Backend |
| PostgreSQL setup | P2 | 4hr | Backend |
| Redis caching | P2 | 3hr | Backend |
| Rate limiting | P3 | 2hr | Backend |

### Mobile Tasks
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Fix Router import | P0 | 5min | Mobile |
| Add error boundaries | P1 | 2hr | Mobile |
| Loading states | P1 | 1hr | Mobile |
| Improve UX | P2 | 4hr | Mobile |
| Widget tests | P2 | 4hr | Mobile |

### CV Tasks
| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Fix division by zero | P0 | 30min | CV |
| Fix GeometryCalculator | P0 | 4hr | CV |
| Add validation | P1 | 2hr | CV |
| Train YOLO | P2 | 40hr | ML |
| Auto-alignment | P2 | 8hr | CV |

---

## TECHNICAL DEBT

| Debt | Priority | Effort | Status |
|------|----------|--------|--------|
| API bugs | P0 | 1hr | Not started |
| Router import | P0 | 5min | Not started |
| GeometryCalculator | P0 | 4hr | Not started |
| Low test coverage | P1 | 8hr | Not started |
| YOLO training | P2 | 40hr | Not started |
| CORS security | P1 | 1hr | Not started |

---

## DEPENDENCIES

```
API Fixes (P0)
    ↓
Stabilization (P1)
    ↓
Features (P2)
    ↓
Optimization (P3)
```

---

## SUCCESS CRITERIA

### Phase 1:
- [ ] API endpoints return valid responses
- [ ] Mobile app starts
- [ ] Manual alignment works
- [ ] Tests pass

### Phase 2:
- [ ] Test coverage > 50%
- [ ] Error handling works
- [ ] Logging works

### Phase 3:
- [ ] Auto-alignment works
- [ ] YOLO model trained
- [ ] Accuracy ±1.5mm
- [ ] PostgreSQL in production

### Phase 4:
- [ ] Performance optimized
- [ ] Scalable architecture

---

## RESOURCES

### Team:
- Backend Developer: 1
- Mobile Developer: 1
- ML/CV Engineer: 1
- QA: 0.5

### Infrastructure:
- PostgreSQL server
- Redis server
- GPU for YOLO training (optional)

---

**Created:** 2026-02-23
**Version:** 4.0.0
**Based on:** KIMI Architecture Analysis v4.0
