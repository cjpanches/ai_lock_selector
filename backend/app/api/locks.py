from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.schemas import LockModelDTO, LocksListResponseDTO

router = APIRouter()

locks_db = []

@router.get("", response_model=LocksListResponseDTO)
async def get_locks(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    limit: Optional[int] = 100,
    offset: int = 0,
):
    filtered = locks_db
    
    if type:
        filtered = [l for l in filtered if l.type == type]
    if brand:
        filtered = [l for l in filtered if l.brand == brand]
    
    return LocksListResponseDTO(
        locks=filtered[offset:offset+limit],
        total=len(filtered),
    )

@router.get("/{lock_id}", response_model=LockModelDTO)
async def get_lock(lock_id: int):
    for lock in locks_db:
        if lock.id == lock_id:
            return lock
    raise HTTPException(status_code=404, detail="Lock not found")

@router.post("")
async def create_lock(lock: LockModelDTO):
    lock.id = len(locks_db) + 1
    locks_db.append(lock)
    return lock

@router.put("/{lock_id}")
async def update_lock(lock_id: int, lock: LockModelDTO):
    for i, l in enumerate(locks_db):
        if l.id == lock_id:
            lock.id = lock_id
            locks_db[i] = lock
            return lock
    raise HTTPException(status_code=404, detail="Lock not found")

@router.delete("/{lock_id}")
async def delete_lock(lock_id: int):
    for i, lock in enumerate(locks_db):
        if lock.id == lock_id:
            locks_db.pop(i)
            return {"message": "Lock deleted"}
    raise HTTPException(status_code=404, detail="Lock not found")
