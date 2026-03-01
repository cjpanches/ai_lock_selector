# Risk Analysis

## Overview

Анализ рисков проекта AI Lock Selector с оценкой вероятности и влияния.

## Risk Register

### Critical Risks (High Impact, High Probability)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | YOLO model not trained | High | High | Prioritize training, use transfer learning |
| R2 | Measurement accuracy < target | Medium | High | Improve CV pipeline, use better calibration |
| R3 | Poor image quality input | High | Medium | Add quality checks, user guidance |

### High Risks (High Impact, Low-Medium Probability)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R4 | PostgreSQL migration issues | Low | High | Test thoroughly, have rollback plan |
| R5 | API rate limiting needed | Medium | High | Implement rate limiting early |
| R6 | Security vulnerabilities | Low | High | Regular security audits |

### Medium Risks (Medium Impact, Medium Probability)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R7 | Flutter performance issues | Medium | Medium | Profile regularly, optimize hot paths |
| R8 | Database performance | Medium | Medium | Add indexes, optimize queries |
| R9 | Mobile camera API changes | Low | Medium | Use stable camera package |

### Low Risks (Low Impact, Any Probability)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R10 | Missing documentation | Medium | Low | Keep docs updated |
| R11 | Test coverage gaps | Medium | Low | Add more tests |
| R12 | Dependencies outdated | Low | Low | Regular updates |

## Detailed Risk Analysis

### R1: YOLO Model Not Trained

**Description**: Модель YOLO не обучена, что делает невозможным автоматические измерения.

**Current State**: Photos collected (762), model not trained

**Impact**:
- Cannot detect lock objects automatically
- Manual measurement required
- Core feature unavailable

**Mitigation**:
1. Upload photos to Roboflow immediately
2. Label all 3 classes
3. Train with pretrained weights (transfer learning)
4. Set up continuous training pipeline

**Timeline**: 1-2 weeks

---

### R2: Measurement Accuracy Below Target

**Description**: Точность измерений не достигает целевых ±0.5-1.0mm.

**Current Target**: ±0.5-1.0mm

**Impact**:
- Incorrect lock recommendations
- Poor user experience
- Potential door compatibility issues

**Root Causes**:
- Poor scale calibration
- Image distortion
- YOLO detection errors

**Mitigation**:
1. Verify scale_factor calculation (use min dimension)
2. Add multiple measurement points
3. Implement confidence scoring
4. Filter low-confidence detections

**Validation**: Test on 50+ diverse images

---

### R3: Poor Image Quality

**Description**: Пользователь предоставляет размытые, темные или неполные изображения.

**Impact**:
- Detection failures
- Inaccurate measurements
- User frustration

**Mitigation**:
1. Pre-capture quality check
2. Real-time feedback to user
3. Auto-enhancement (brightness, contrast)
4. Clear instructions

**UI Implementation**:
- "Image too dark" warning
- "Move closer" suggestion
- Capture button disabled until good quality

---

### R4: PostgreSQL Migration Issues

**Description**: Переход с SQLite на PostgreSQL вызывает проблемы.

**Current**: SQLite (works fine for 147 locks)

**Impact**:
- Downtime
- Data loss
- Performance regression

**Mitigation**:
1. Test migration in staging
2. Keep SQLite as fallback
3. Detailed rollback plan
4. Migrate after v1.0

---

### R5: API Rate Limiting Needed

**Description**: API становится мишенью для злоупотреблений.

**Current**: No rate limiting

**Impact**:
- Service degradation
- Resource exhaustion
- Cost overruns

**Mitigation**:
1. Implement rate limiting (100 req/hour per IP)
2. Add API key for authenticated users
3. Monitor usage patterns

---

## Risk Matrix

```
Impact
  High  │  R1,R2   │  R4,R5,R6│
        │          │          │
 Medium │  R3,R7,R8│  R9      │
        │          │          │
 Low    │ R10,R11  │  R12     │
        └──────────┴──────────┘
         Low    Medium   High
              Probability
```

## Monitoring

### Key Metrics
- API response time (<200ms p95)
- Detection success rate (>90%)
- Measurement accuracy (±1mm)
- User satisfaction (>4 stars)

### Alerts
- Detection success <80%
- API error rate >5%
- DB query time >500ms

## Contingency Plans

| Scenario | Backup Plan |
|----------|-------------|
| YOLO not ready | Manual measurement mode |
| DB down | Cached responses |
| API overloaded | Graceful degradation |
| CV fails | User input fallback |

## Related Documents

- [COMPREHENSIVE_AUDIT_v4.4.md](./COMPREHENSIVE_AUDIT_v4.4.md) - Full audit
- [15_DEVELOPMENT_PLAN.md](./15_DEVELOPMENT_PLAN.md) - Development plan
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Current status
