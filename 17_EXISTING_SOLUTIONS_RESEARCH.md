# Existing Solutions Research

## Overview

Обзор существующих решений и продуктов в области умных замков и измерительных инструментов.

## Competitor Products

### 1. DoorBird

**Description**: German smart door intercom system with camera

**Website**: doorbird.com

**Features**:
- Camera-based access control
- Mobile app integration
- Cloud connectivity
- Motion detection
- Keyless entry

**Analysis**:
- Focus on access control, not measurement
- No AR measurement capability
- Premium pricing (€300-500)

**Relevance**: Different use case - access control vs measurement

---

### 2. Nuki

**Description**: European smart lock company

**Website**: nuki.io

**Features**:
- Smart lock retrofit
- Auto unlock
- Access sharing
- Integration with smart home

**Analysis**:
- Hardware-focused (smart lock)
- No camera/measurement features
- Strong European presence

**Relevance**: Complementary product, not competitor

---

### 3. Aqara

**Description**: Chinese smart home ecosystem

**Website**: aqara.com

**Features**:
- Smart locks
- Sensors
- Camera hub
- Matter support

**Analysis**:
- Budget-friendly
- No specialized measurement
- Good integration ecosystem

**Relevance**: Similar smart home, different focus

---

### 4. Yale

**Description**: Traditional lock manufacturer going smart

**Website**: yalehome.com

**Features**:
- Smart locks
- Biometric access
- Keypad options

**Analysis**:
- Brand trust
- No measurement feature
- Retail-focused

**Relevance**: Major player in lock market

---

## Measurement Apps (Direct Competitors)

### 1. Measure App (Apple)

**Features**:
- AR-based measurement
- Point-to-point measuring
- Object detection

**Limitations**:
- General purpose, not lock-specific
- No database matching
- No AR overlay for euro cylinder

**Our Advantage**: Specialized for locks with database matching

---

### 2. Google Measure

**Features**:
- AR measurement
- Camera-based
- Works on Android

**Limitations**:
- General purpose
- No lock-specific features

**Our Advantage**: Lock-focused with brand matching

---

## Technical Solutions

### CV Libraries Comparison

| Library | Pros | Cons |
|---------|------|------|
| OpenCV | Mature, fast | Complex API |
| MediaPipe | Google support | Limited features |
| TensorFlow Lite | Mobile-optimized | Higher latency |
| YOLOv8 | State-of-art detection | Requires training |

**Decision**: YOLOv8 + OpenCV (current stack)

---

### AR Frameworks

| Framework | Platform | Pros |
|-----------|----------|------|
| ARKit | iOS | Native, performant |
| ARCore | Android | Native, performant |
| Flutter AR | Cross-platform | Easy, but limited |
| WebXR | Web | Browser-based |

**Decision**: Flutter + camera package (cross-platform)

---

## Market Gaps

### Identified Opportunities

1. **Lock Measurement Apps**: No dedicated lock measurement with matching
2. **Database Integration**: None combine measurement with product DB
3. **AR Calibration**: Euro cylinder as scale reference is novel
4. **Russian Market**: Few localized solutions

### Competitive Advantages

| Feature | DoorBird | Nuki | Yale | Our Solution |
|---------|----------|------|------|--------------|
| Lock Measurement | ❌ | ❌ | ❌ | ✅ |
| AR Overlay | ❌ | ❌ | ❌ | ✅ |
| Database Matching | ❌ | ❌ | ❌ | ✅ |
| Euro Cylinder Focus | ❌ | ❌ | ❌ | ✅ |
| Russian Language | ❌ | ⚠️ | ⚠️ | ✅ |

---

## Lessons Learned

### From Competitors

1. **Focus on reliability** - Users trust established lock brands
2. **Integration matters** - Smart home ecosystems increase value
3. **User experience** - Simple installation and setup
4. **Mobile-first** - App is primary interface

### From Measurement Apps

1. **AR works** - Users understand AR overlays
2. **Calibration needed** - Reference objects improve accuracy
3. **Feedback important** - Show confidence levels

---

## References

- DoorBird: https://www.doorbird.com/
- Nuki: https://nuki.io/
- Aqara: https://www.aqara.com/
- Yale: https://www.yalehome.com/
- Apple Measure: https://support.apple.com/en-us/102672
- Google Measure: (deprecated)

## Related Documents

- [05_AR_MEASUREMENT_TECH.md](./05_AR_MEASUREMENT_TECH.md) - AR implementation
- [06_CV_MODEL_SPEC.md](./06_CV_MODEL_SPEC.md) - CV implementation
- [01_REQUIREMENTS.md](./01_REQUIREMENTS.md) - Project requirements
