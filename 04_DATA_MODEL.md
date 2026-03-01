# Data Model

## Database Overview

- **Engine**: SQLite (async via aiosqlite)
- **Location**: `backend/locks.db`
- **Tables**: 4

## Tables

### 1. manufacturers

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String(255) | Manufacturer name |
| country | String(100) | Country of origin |
| website | String(500) | Manufacturer website |
| created_at | DateTime | Creation timestamp |

### 2. locks

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| vendor_code | String(50) | Unique vendor code (indexed) |
| name | String(255) | Lock name |
| description | Text | Full description |
| brand | String(100) | Brand name (indexed) |
| series | String(50) | Series name |
| color | String(20) | Lock color |
| manufacturer_id | Integer | FK to manufacturers |

**Type & Dimensions:**
| Column | Type | Description |
|--------|------|-------------|
| type | Enum | embedded, overlay, latch, deadbolt, electronic, cylinder |
| backset | Float | Backset in mm (required) |
| center_distance | Float | Center distance in mm (required) |
| plate_width | Float | Plate width in mm |
| plate_height | Float | Plate height in mm |
| plate_thickness | Float | Plate thickness in mm |

**Body Dimensions:**
| Column | Type | Description |
|--------|------|-------------|
| body_width | Float | Body width in mm |
| body_height | Float | Body height in mm |
| body_depth | Float | Body depth in mm |

**Hole Specifications:**
| Column | Type | Description |
|--------|------|-------------|
| lock_cylinder_hole | String(20) | Cylinder hole type |
| square_hole_size | Float | Handle square size (mm) |

**Package Info:**
| Column | Type | Description |
|--------|------|-------------|
| package_type | String(20) | Package type |
| package_qty | Integer | Quantity in package |
| minibox_qty | Integer | Minibox quantity |

**Usage:**
| Column | Type | Description |
|--------|------|-------------|
| purpose | String(50) | Purpose |
| for_entry_doors | String(10) | For entry doors |
| for_interior_doors | String(10) | For interior doors |
| mounting_type | String(50) | Mounting type |

**Bolt:**
| Column | Type | Description |
|--------|------|-------------|
| bolt_type | String(50) | Bolt type |
| bolt_count | Integer | Number of bolts |
| bolt_throw | Float | Bolt throw (mm) |
| bolt_diameter | Float | Bolt diameter (mm) |

**Cylinder:**
| Column | Type | Description |
|--------|------|-------------|
| mechanism_type | String(50) | Mechanism type |
| key_type | String(50) | Key type |
| key_count | Integer | Number of keys |
| cylinder_included | String(20) | Cylinder included |
| cylinder_size | String(20) | Cylinder size |
| cylinder_material | String(50) | Cylinder material |

**Media:**
| Column | Type | Description |
|--------|------|-------------|
| image_url | String(500) | Product image URL |
| drawing_url | String(500) | Drawing URL |

### 3. lock_compatibility

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| lock_id | Integer | FK to locks |
| compatible_cylinder_id | Integer | FK to compatible cylinder |
| compatibility_type | String(50) | Type of compatibility |

### 4. measurements

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| lock_id | Integer | FK to locks |
| measured_backset | Float | Measured backset |
| measured_center_distance | Float | Measured center distance |
| measured_at | DateTime | Measurement timestamp |
| image_path | String(500) | Path to measured image |

## Enum: LockTypeEnum

```python
class LockTypeEnum(str, enum.Enum):
    embedded = "embedded"    # Врезной
    overlay = "overlay"      # Накладной
    latch = "latch"          # Защелка
    deadbolt = "deadbolt"   # Ригель
    electronic = "electronic" # Электронный
    cylinder = "cylinder"    # Цилиндровый
```

## Relationships

```
Manufacturer (1) ───▶ (N) Lock
Lock (1) ───▶ (N) LockCompatibility
Lock (1) ───▶ (N) Measurement
```

## Current Statistics

- **Manufacturers**: ~10+
- **Locks**: 147
- **Lock Types**: embedded, overlay, latch, deadbolt, electronic, cylinder

## Data Ranges

| Parameter | Min | Max |
|-----------|-----|-----|
| Backset (mm) | 20 | 68 |
| Center Distance (mm) | 50 | 92 |
| Plate Width (mm) | 3 | 8 |
| Square Size (mm) | 8 | 10 |

## Related Documents

- [08_API_SPEC.md](./08_API_SPEC.md) - API спецификация
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Технические параметры
