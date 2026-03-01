# API Specification

## Base URL
```
http://127.0.0.1:8001
```

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/locks` | List all locks |
| POST | `/api/v1/locks` | Create new lock |
| GET | `/api/v1/locks/{id}` | Get lock by ID |
| PUT | `/api/v1/locks/{id}` | Update lock |
| DELETE | `/api/v1/locks/{id}` | Delete lock |
| POST | `/api/v1/measure` | Measure lock from image |
| POST | `/api/v1/match` | Find matching locks |
| POST | `/api/v1/cv/process` | Process image with CV |
| GET | `/health` | Health check |

---

## Locks Endpoints

### GET /api/v1/locks
Get list of locks with optional filters.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by lock type |
| brand | string | Filter by brand |
| limit | int | Number of results (default: 100) |
| offset | int | Pagination offset |

**Response:**
```json
{
  "locks": [
    {
      "id": 1,
      "vendor_code": "APECS-1026-60",
      "name": "Замок врезной Apecs 1026/60-G",
      "brand": "Apecs",
      "type": "embedded",
      "backset": 45.0,
      "center_distance": 72.0,
      "plate_width": 5.5,
      "plate_height": 235.0
    }
  ],
  "total": 147
}
```

### GET /api/v1/locks/{lock_id}
Get single lock by ID.

**Response:**
```json
{
  "id": 1,
  "vendor_code": "APECS-1026-60",
  "name": "Замок врезной Apecs 1026/60-G",
  "brand": "Apecs",
  "type": "embedded",
  "backset": 45.0,
  "center_distance": 72.0,
  "plate_width": 5.5,
  "plate_height": 235.0,
  "plate_thickness": 3.0,
  "body_width": 65.0,
  "body_height": 150.0,
  "body_depth": 14.0,
  "cylinder_hole": "DIN",
  "square_hole_size": 8.0,
  "description": "..."
}
```

### POST /api/v1/locks
Create new lock.

**Request Body:** Same as GET response

---

## Measurement Endpoints

### POST /api/v1/measure
Measure lock parameters from image.

**Request:**
```json
{
  "image": "base64_encoded_image"
}
```

**Response:**
```json
{
  "backset_mm": 45.2,
  "center_distance_mm": 72.0,
  "plate_width_mm": 5.5,
  "plate_height_mm": 235.0,
  "confidence": 0.89,
  "scale_factor": 12.5,
  "detected_classes": {
    "lock_plate": {"x": 100, "y": 50, "w": 200, "h": 400},
    "cylinder_hole": {"x": 150, "y": 100, "w": 30, "h": 100},
    "handle_square": {"x": 150, "y": 300, "w": 20, "h": 20}
  }
}
```

### POST /api/v1/match
Find matching locks from measured profile.

**Request:**
```json
{
  "backset": 45.0,
  "center_distance": 72.0,
  "plate_width": 5.5
}
```

**Response:**
```json
{
  "matches": [
    {
      "lock": {
        "id": 1,
        "name": "Замок врезной Apecs 1026/60-G",
        "brand": "Apecs"
      },
      "score": 0.95,
      "matched_params": {
        "backset": {"measured": 45.0, "database": 45.0, "diff": 0.0},
        "center_distance": {"measured": 72.0, "database": 72.0, "diff": 0.0}
      }
    }
  ]
}
```

---

## CV Endpoints

### POST /api/v1/cv/process
Process image with CV pipeline.

**Request:**
```json
{
  "image": "base64_encoded_image"
}
```

**Response:**
```json
{
  "detections": [
    {"class": "lock_plate", "confidence": 0.95, "bbox": [...]},
    {"class": "cylinder_hole", "confidence": 0.92, "bbox": [...]},
    {"class": "handle_square", "confidence": 0.88, "bbox": [...]}
  ],
  "measurements": {...}
}
```

---

## Health Check

### GET /health

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Error Responses

All endpoints may return:

| Status | Description |
|--------|-------------|
| 400 | Bad Request - invalid parameters |
| 404 | Not Found - resource doesn't exist |
| 500 | Internal Server Error |

**Error Format:**
```json
{
  "detail": "Error message description"
}
```

---

## Related Documents

- [backend/app/main.py](../backend/app/main.py) - FastAPI app
- [backend/app/api/](../backend/app/api/) - API route handlers
- [12_MATCHING_ALGORITHM.md](./12_MATCHING_ALGORITHM.md) - Matching logic
