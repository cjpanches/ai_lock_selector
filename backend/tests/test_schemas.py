import pytest
from app.models.schemas import (
    LockType,
    LockDimensionsDTO,
    LockModelDTO,
    LockProfileDTO,
    MountingHoleDTO,
)


class TestLockSchemas:
    def test_lock_type_enum(self):
        assert LockType.embedded.value == "embedded"
        assert LockType.overlay.value == "overlay"
        assert LockType.latch.value == "latch"

    def test_lock_dimensions_dto(self):
        dims = LockDimensionsDTO(
            backset=55.0,
            center_distance=72.0,
            plate_width=24.0,
            plate_height=235.0,
            plate_thickness=3.0,
            body_width=85.0,
            body_height=165.0,
            body_depth=13.0,
        )
        assert dims.backset == 55.0
        assert dims.plate_height == 235.0

    def test_lock_model_dto(self):
        lock = LockModelDTO(
            id=1,
            vendor_code="A-001",
            name="Test Lock",
            brand="TestBrand",
            type=LockType.embedded,
            backset=55.0,
            center_distance=72.0,
            plate_width=24.0,
            plate_height=235.0,
            plate_thickness=3.0,
            body_width=85.0,
            body_height=165.0,
            body_depth=13.0,
        )
        assert lock.vendor_code == "A-001"
        assert lock.type == LockType.embedded

    def test_mounting_hole_dto(self):
        hole = MountingHoleDTO(
            x=10.0,
            y=20.0,
            diameter=6.0,
        )
        assert hole.diameter == 6.0

    def test_lock_profile_dto(self):
        profile = LockProfileDTO(
            dimensions=LockDimensionsDTO(
                backset=55.0,
                center_distance=72.0,
                plate_width=24.0,
                plate_height=235.0,
                plate_thickness=3.0,
                body_width=85.0,
                body_height=165.0,
                body_depth=13.0,
            ),
            mounting_holes=[
                MountingHoleDTO(x=10.0, y=20.0, diameter=6.0),
            ],
            confidence=0.85,
            captured_at="2026-02-22T10:00:00",
        )
        assert profile.confidence == 0.85
        assert len(profile.mounting_holes) == 1


class TestLockModelValidation:
    def test_optional_fields(self):
        lock = LockModelDTO(
            vendor_code="A-001",
            name="Minimal Lock",
            type=LockType.latch,
            backset=0.0,
            center_distance=0.0,
            plate_width=22.0,
            plate_height=150.0,
            plate_thickness=2.5,
            body_width=65.0,
            body_height=100.0,
            body_depth=12.0,
        )
        assert lock.id is None
        assert lock.image_url is None
