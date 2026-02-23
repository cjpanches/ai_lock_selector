from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import (
    LockModelDTO, 
    LocksListResponseDTO,
    MeasureResponseDTO,
    LockProfileDTO,
    MatchResponseDTO,
    LockMatchDTO,
    MatchResultDTO,
)
from app.services.measurement_service import MeasurementService
from app.services.matching_service import MatchingService

router = APIRouter()

measurement_service = MeasurementService()
matching_service = MatchingService()

@router.post("/measure", response_model=MeasureResponseDTO)
async def measure_lock(request: dict):
    """Обработка изображения и измерение параметров замка"""
    try:
        profile = await measurement_service.process_measurement(
            image_base64=request.get("image"),
            scale_factor=request.get("scale_factor"),
            marker_x=request.get("marker_x"),
            marker_y=request.get("marker_y"),
        )
        return MeasureResponseDTO(profile=profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match", response_model=MatchResponseDTO)
async def match_lock(profile: LockProfileDTO, db: AsyncSession = Depends(get_db)):
    """Подбор аналогов замка по измеренным параметрам"""
    try:
        matches = await matching_service.find_matches(profile, db)
        return MatchResponseDTO(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=LocksListResponseDTO)
async def get_locks(
    type: Optional[str] = None,
    brand: Optional[str] = None,
    limit: Optional[int] = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Получение списка замков"""
    locks = await matching_service.get_locks_from_db(
        db=db,
        type=type,
        brand=brand,
        limit=limit,
        offset=offset,
    )
    return LocksListResponseDTO(locks=locks, total=len(locks))

@router.get("/{lock_id}", response_model=LockModelDTO)
async def get_lock(lock_id: int, db: AsyncSession = Depends(get_db)):
    """Получение конкретного замка по ID"""
    lock = await matching_service.get_lock_by_id(db, lock_id)
    if not lock:
        raise HTTPException(status_code=404, detail="Lock not found")
    return lock
