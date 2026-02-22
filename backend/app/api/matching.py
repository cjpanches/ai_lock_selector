from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import MatchResponseDTO, LockProfileDTO
from app.services.matching_service import matching_service

router = APIRouter()


@router.post("", response_model=MatchResponseDTO)
async def match_lock(profile: LockProfileDTO, db: AsyncSession = Depends(get_db)):
    """Подбор аналогов замка по измеренным параметрам"""
    try:
        matches = await matching_service.find_matches(profile, db)
        return MatchResponseDTO(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
