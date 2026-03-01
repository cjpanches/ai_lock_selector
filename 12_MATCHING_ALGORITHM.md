# Matching Algorithm

## Overview

Fuzzy matching алгоритм для подбора аналогов замков по измеренным параметрам.

## Problem Statement

Пользователь измеряет замок по фото и получает параметры:
- Backset (мм)
- Center Distance (мм)
- Plate Width (мм)
- Plate Height (мм)

Необходимо найти в базе данных замки с наиболее близкими параметрами.

## Tolerances

| Parameter | Tolerance | Weight |
|-----------|-----------|--------|
| Backset | ±2mm | 35% |
| Center Distance | ±3mm | 30% |
| Plate Width | ±2mm | 15% |
| Plate Height | ±3mm | 10% |
| Body Width | ±5mm | 5% |
| Body Height | ±5mm | 5% |

### Why These Values?

- **Backset** (35%): Most critical - determines door compatibility
- **Center Distance** (30%): Second most important - handle position
- **Plate Width** (15%): Visual match
- **Plate Height** (10%): General size match
- **Body Dimensions** (5% each): Additional verification

## Score Calculation

### Formula

```python
def calculate_match_score(measured, database_lock):
    score = 0.0
    
    # Backset (35%)
    backset_diff = abs(measured.backset - database_lock.backset)
    if backset_diff <= TOLERANCE['backset']:
        score += WEIGHTS['backset'] * (1 - backset_diff / TOLERANCE['backset'])
    
    # Center Distance (30%)
    distance_diff = abs(measured.center_distance - database_lock.center_distance)
    if distance_diff <= TOLERANCE['center_distance']:
        score += WEIGHTS['center_distance'] * (1 - distance_diff / TOLERANCE['center_distance'])
    
    # Plate Width (15%)
    width_diff = abs(measured.plate_width - database_lock.plate_width)
    if width_diff <= TOLERANCE['plate_width']:
        score += WEIGHTS['plate_width'] * (1 - width_diff / TOLERANCE['plate_width'])
    
    # Plate Height (10%)
    height_diff = abs(measured.plate_height - database_lock.plate_height)
    if height_diff <= TOLERANCE['plate_height']:
        score += WEIGHTS['plate_height'] * (1 - height_diff / TOLERANCE['plate_height'])
    
    return score
```

### Score Range

- **0.0 - 1.0**: Where 1.0 is perfect match
- **> 0.3**: Include in results (threshold)
- **> 0.8**: Excellent match (highlighted)
- **> 0.95**: Near-exact match (virtually identical)

## Implementation

### Backend Service
```python
# backend/app/services/matching_service.py
class MatchingService:
    TOLERANCES = {
        "backset": 2.0,
        "center_distance": 3.0,
        "plate_width": 2.0,
        "plate_height": 3.0,
        "body_width": 5.0,
        "body_height": 5.0,
    }
    
    WEIGHTS = {
        "backset": 0.35,
        "center_distance": 0.30,
        "plate_width": 0.15,
        "plate_height": 0.10,
        "body_width": 0.05,
        "body_height": 0.05,
    }
```

### API Endpoint

```python
@router.post("/api/v1/match")
async def match_lock(profile: LockProfileDTO, db: AsyncSession):
    matches = await matching_service.find_matches(profile, db)
    return {"matches": matches}
```

## Result Format

```json
{
  "matches": [
    {
      "lock": {
        "id": 1,
        "name": "Замок Apecs 1026/60-G",
        "brand": "Apecs",
        "backset": 45.0,
        "center_distance": 72.0
      },
      "score": 0.95,
      "matched_params": {
        "backset": {
          "measured": 45.2,
          "database": 45.0,
          "diff": 0.2,
          "within_tolerance": true
        },
        "center_distance": {
          "measured": 72.0,
          "database": 72.0,
          "diff": 0.0,
          "within_tolerance": true
        }
      }
    }
  ]
}
```

## Sorting

Results sorted by:
1. **Score** (descending) - Best match first
2. **Backset diff** (ascending) - Within tolerance preferred
3. **Brand** (alphabetical) - For consistency

## Optimization

### Current Approach
- Scan all 147 locks
- Calculate score for each
- Sort and return top 10

### Future Optimizations
- Index on backset and center_distance
- Pre-filter by type (embedded, overlay)
- Cache frequent queries
- Use approximate nearest neighbor

## Testing

```bash
cd backend
pytest tests/test_matching.py -v
```

Tests verify:
- Tolerances defined correctly
- Weights sum to 1.0
- Score calculation accuracy
- Threshold filtering

## Related Documents

- [backend/app/services/matching_service.py](../backend/app/services/matching_service.py) - Implementation
- [backend/tests/test_matching.py](../backend/tests/test_matching.py) - Tests
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Technical details
