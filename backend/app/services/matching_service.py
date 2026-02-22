from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Lock
from app.models.schemas import LockProfileDTO, LockModelDTO, LockMatchDTO, MatchResultDTO

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


class MatchingService:
    def __init__(self):
        self.tolerance_map = TOLERANCES
        self.weights = WEIGHTS
    
    async def find_matches(self, profile: LockProfileDTO, db: AsyncSession) -> list[LockMatchDTO]:
        """Поиск аналогов замка по измеренным параметрам"""
        
        result = await db.execute(select(Lock).limit(100))
        locks = result.scalars().all()
        
        matches = []
        dims = profile.dimensions
        
        for lock in locks:
            score = self._calculate_match_score(dims, lock)
            
            if score > 0.3:
                matched_params = self._get_matched_params(dims, lock)
                lock_dto = self._lock_to_dto(lock)
                matches.append(LockMatchDTO(
                    lock=lock_dto,
                    score=score,
                    matched_params=matched_params,
                ))
        
        matches.sort(key=lambda m: m.score, reverse=True)
        
        return matches[:10]
    
    def _calculate_match_score(self, dims, lock) -> float:
        """Расчёт score совпадения"""
        score = 0
        total_weight = 0
        
        score += self._calculate_param_score(dims.backset, lock.backset, "backset")
        total_weight += self.weights["backset"]
        
        score += self._calculate_param_score(dims.center_distance, lock.center_distance, "center_distance")
        total_weight += self.weights["center_distance"]
        
        score += self._calculate_param_score(dims.plate_width, lock.plate_width, "plate_width")
        total_weight += self.weights["plate_width"]
        
        score += self._calculate_param_score(dims.plate_height, lock.plate_height, "plate_height")
        total_weight += self.weights["plate_height"]
        
        score += self._calculate_param_score(dims.body_width, lock.body_width, "body_width", tolerance=5.0)
        total_weight += self.weights["body_width"]
        
        score += self._calculate_param_score(dims.body_height, lock.body_height, "body_height", tolerance=5.0)
        total_weight += self.weights["body_height"]
        
        return score / total_weight if total_weight > 0 else 0
    
    def _calculate_param_score(self, profile_value, lock_value, param, tolerance=None):
        """Расчёт score для одного параметра"""
        tol = tolerance or self.tolerance_map.get(param, 2.0)
        weight = self.weights.get(param, 0.1)
        
        if profile_value == 0 or lock_value is None or lock_value == 0:
            return 0
        
        diff = abs(profile_value - lock_value)
        
        if diff <= tol:
            return weight * (1 - (diff / tol) * 0.5)
        elif diff <= tol * 2:
            return weight * 0.25 * (1 - (diff - tol) / tol)
        
        return 0
    
    def _get_matched_params(self, dims, lock) -> dict:
        """Получение информации о совпадении параметров"""
        return {
            "backset": MatchResultDTO(
                measured=dims.backset,
                expected=lock.backset,
                deviation=dims.backset - lock.backset,
                is_within_tolerance=abs(dims.backset - lock.backset) <= self.tolerance_map["backset"],
            ),
            "center_distance": MatchResultDTO(
                measured=dims.center_distance,
                expected=lock.center_distance,
                deviation=dims.center_distance - lock.center_distance,
                is_within_tolerance=abs(dims.center_distance - lock.center_distance) <= self.tolerance_map["center_distance"],
            ),
            "plate_width": MatchResultDTO(
                measured=dims.plate_width,
                expected=lock.plate_width,
                deviation=dims.plate_width - lock.plate_width,
                is_within_tolerance=abs(dims.plate_width - lock.plate_width) <= self.tolerance_map["plate_width"],
            ),
        }
    
    def _lock_to_dto(self, lock: Lock) -> LockModelDTO:
        return LockModelDTO(
            id=lock.id,
            vendor_code=lock.vendor_code,
            name=lock.name,
            brand=lock.brand,
            type=lock.type.value,
            backset=lock.backset,
            center_distance=lock.center_distance,
            plate_width=lock.plate_width,
            plate_height=lock.plate_height,
            plate_thickness=lock.plate_thickness,
            body_width=lock.body_width,
            body_height=lock.body_height,
            body_depth=lock.body_depth,
            cylinder_hole=lock.lock_cylinder_hole,
            square_hole_size=lock.square_hole_size,
            image_url=lock.image_url,
            drawing_url=lock.drawing_url,
            description=lock.description,
        )


matching_service = MatchingService()
