from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.database import get_db
from app.db.models import Lock, LockTypeEnum
from app.models.schemas import LockModelDTO, LocksListResponseDTO, LockType

router = APIRouter()


def lock_to_dto(lock: Lock) -> LockModelDTO:
    return LockModelDTO(
        id=lock.id,
        vendor_code=lock.vendor_code,
        name=lock.name,
        brand=lock.brand,
        type=LockType(lock.type.value),
        backset=lock.backset,
        center_distance=lock.center_distance,
        plate_width=lock.plate_width,
        plate_height=lock.plate_height,
        plate_thickness=lock.plate_thickness,
        body_width=lock.body_width,
        body_height=lock.body_height,
        body_depth=lock.body_depth,
        cylinder_hole_diameter=lock.cylinder_hole_diameter,
        square_hole_size=lock.square_hole_size,
        image_url=lock.image_url,
        drawing_url=lock.drawing_url,
        description=lock.description,
    )


@router.get("", response_model=LocksListResponseDTO)
async def get_locks(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(Lock)
    
    if type:
        query = query.where(Lock.type == LockTypeEnum(type))
    if brand:
        query = query.where(Lock.brand == brand)
    
    count_query = select(Lock)
    if type:
        count_query = count_query.where(Lock.type == LockTypeEnum(type))
    if brand:
        count_query = count_query.where(Lock.brand == brand)
    
    from sqlalchemy import func
    total_result = await db.execute(select(func.count()).select_from(count_query.subquery()))
    total = total_result.scalar() or 0
    
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    locks = result.scalars().all()
    
    return LocksListResponseDTO(
        locks=[lock_to_dto(lock) for lock in locks],
        total=total,
    )


@router.get("/{lock_id}", response_model=LockModelDTO)
async def get_lock(lock_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lock).where(Lock.id == lock_id))
    lock = result.scalar_one_or_none()
    if not lock:
        raise HTTPException(status_code=404, detail="Lock not found")
    return lock_to_dto(lock)


@router.post("", response_model=LockModelDTO)
async def create_lock(lock: LockModelDTO, db: AsyncSession = Depends(get_db)):
    db_lock = Lock(
        vendor_code=lock.vendor_code,
        name=lock.name,
        brand=lock.brand,
        type=LockTypeEnum(lock.type.value),
        backset=lock.backset,
        center_distance=lock.center_distance,
        plate_width=lock.plate_width,
        plate_height=lock.plate_height,
        plate_thickness=lock.plate_thickness,
        body_width=lock.body_width,
        body_height=lock.body_height,
        body_depth=lock.body_depth,
        cylinder_hole_diameter=lock.cylinder_hole_diameter,
        square_hole_size=lock.square_hole_size,
        image_url=lock.image_url,
        drawing_url=lock.drawing_url,
        description=lock.description,
    )
    db.add(db_lock)
    await db.commit()
    await db.refresh(db_lock)
    return lock_to_dto(db_lock)


@router.put("/{lock_id}", response_model=LockModelDTO)
async def update_lock(lock_id: int, lock: LockModelDTO, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lock).where(Lock.id == lock_id))
    db_lock = result.scalar_one_or_none()
    if not db_lock:
        raise HTTPException(status_code=404, detail="Lock not found")
    
    db_lock.vendor_code = lock.vendor_code
    db_lock.name = lock.name
    db_lock.brand = lock.brand
    db_lock.type = LockTypeEnum(lock.type.value)
    db_lock.backset = lock.backset
    db_lock.center_distance = lock.center_distance
    db_lock.plate_width = lock.plate_width
    db_lock.plate_height = lock.plate_height
    db_lock.plate_thickness = lock.plate_thickness
    db_lock.body_width = lock.body_width
    db_lock.body_height = lock.body_height
    db_lock.body_depth = lock.body_depth
    db_lock.cylinder_hole_diameter = lock.cylinder_hole_diameter
    db_lock.square_hole_size = lock.square_hole_size
    db_lock.image_url = lock.image_url
    db_lock.drawing_url = lock.drawing_url
    db_lock.description = lock.description
    
    await db.commit()
    await db.refresh(db_lock)
    return lock_to_dto(db_lock)


@router.delete("/{lock_id}")
async def delete_lock(lock_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lock).where(Lock.id == lock_id))
    lock = result.scalar_one_or_none()
    if not lock:
        raise HTTPException(status_code=404, detail="Lock not found")
    await db.delete(lock)
    await db.commit()
    return {"message": "Lock deleted"}
