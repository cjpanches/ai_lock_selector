from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class LockType(str, Enum):
    embedded = "embedded"
    overlay = "overlay"
    latch = "latch"
    deadbolt = "deadbolt"
    electronic = "electronic"
    cylinder = "cylinder"

class LockDimensionsDTO(BaseModel):
    backset: float
    center_distance: float
    plate_width: float
    plate_height: float
    plate_thickness: float
    body_width: float
    body_height: float
    body_depth: float

class MountingHoleDTO(BaseModel):
    x: float
    y: float
    diameter: float

class HandleSquarePositionDTO(BaseModel):
    x: float
    y: float
    size: float

class CylinderHolePositionDTO(BaseModel):
    x: float
    y: float
    width: float
    height: float

class LockProfileDTO(BaseModel):
    id: Optional[str] = None
    dimensions: LockDimensionsDTO
    mounting_holes: List[MountingHoleDTO]
    handle_square: Optional[HandleSquarePositionDTO] = None
    cylinder_hole: Optional[CylinderHolePositionDTO] = None
    confidence: float
    captured_at: str
    image_path: Optional[str] = None

class LockModelDTO(BaseModel):
    id: Optional[int] = None
    vendor_code: str
    name: str
    brand: Optional[str] = None
    type: LockType
    backset: float
    center_distance: float
    plate_width: Optional[float] = None
    plate_height: Optional[float] = None
    plate_thickness: Optional[float] = None
    body_width: Optional[float] = None
    body_height: Optional[float] = None
    body_depth: Optional[float] = None
    cylinder_hole: Optional[str] = None
    square_hole_size: Optional[float] = None
    image_url: Optional[str] = None
    drawing_url: Optional[str] = None
    description: Optional[str] = None
    compatible_with: Optional[List[str]] = None
    updated_at: Optional[str] = None

class MatchResultDTO(BaseModel):
    measured: float
    expected: float
    deviation: float
    is_within_tolerance: bool

class LockMatchDTO(BaseModel):
    lock: LockModelDTO
    score: float
    matched_params: dict[str, MatchResultDTO]

class MeasureRequestDTO(BaseModel):
    image: str
    scale_factor: float
    marker_x: Optional[float] = None
    marker_y: Optional[float] = None

class MeasureResponseDTO(BaseModel):
    profile: LockProfileDTO

class MatchResponseDTO(BaseModel):
    matches: List[LockMatchDTO]

class LocksListResponseDTO(BaseModel):
    locks: List[LockModelDTO]
    total: int
