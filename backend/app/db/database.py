from app.models.schemas import LockModelDTO, LockType

sample_locks = [
    LockModelDTO(
        id=1,
        vendor_code="A-001",
        name="Замок врезной A",
        brand="SecureLock",
        type=LockType.embedded,
        backset=55.0,
        center_distance=72.0,
        plate_width=24.0,
        plate_height=235.0,
        plate_thickness=3.0,
        body_width=85.0,
        body_height=165.0,
        body_depth=13.0,
        cylinder_hole_diameter=50.0,
        square_hole_size=8.0,
    ),
    LockModelDTO(
        id=2,
        vendor_code="A-002",
        name="Замок врезной B",
        brand="SecureLock",
        type=LockType.embedded,
        backset=72.0,
        center_distance=85.0,
        plate_width=24.0,
        plate_height=235.0,
        plate_thickness=3.0,
        body_width=85.0,
        body_height=165.0,
        body_depth=13.0,
        cylinder_hole_diameter=50.0,
        square_hole_size=8.0,
    ),
    LockModelDTO(
        id=3,
        vendor_code="B-001",
        name="Замок накладной",
        brand="DoorGuard",
        type=LockType.overlay,
        backset=0.0,
        center_distance=0.0,
        plate_width=35.0,
        plate_height=180.0,
        plate_thickness=5.0,
        body_width=90.0,
        body_height=130.0,
        body_depth=40.0,
    ),
    LockModelDTO(
        id=4,
        vendor_code="C-001",
        name="Защёлка",
        brand="SimpleLock",
        type=LockType.latch,
        backset=0.0,
        center_distance=0.0,
        plate_width=22.0,
        plate_height=150.0,
        plate_thickness=2.5,
        body_width=65.0,
        body_height=100.0,
        body_depth=12.0,
        square_hole_size=8.0,
    ),
]

async def get_locks(type=None, brand=None, limit=100, offset=0):
    filtered = sample_locks
    
    if type:
        filtered = [l for l in filtered if l.type.value == type]
    if brand:
        filtered = [l for l in filtered if l.brand == brand]
    
    return filtered[offset:offset+limit]

async def get_lock_by_id(lock_id: int):
    for lock in sample_locks:
        if lock.id == lock_id:
            return lock
    return None
