from fastapi import HTTPException
from app.models.schemas import MatchResponseDTO, LockMatchDTO, LockProfileDTO, MatchResultDTO
from app.services.matching_service import MatchingService
from fastapi import APIRouter

router = APIRouter()
matching_service = MatchingService()

@router.post("", response_model=MatchResponseDTO)
async def match_lock(profile: LockProfileDTO):
    """Подбор аналогов замка по измеренным параметрам"""
    try:
        matches = await matching_service.find_matches(profile)
        return MatchResponseDTO(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
