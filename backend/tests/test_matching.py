import pytest
from app.services.matching_service import MatchingService, TOLERANCES, WEIGHTS


class TestMatchingService:
    def setup_method(self):
        self.service = MatchingService()

    def test_tolerances_defined(self):
        assert "backset" in TOLERANCES
        assert "center_distance" in TOLERANCES
        assert TOLERANCES["backset"] == 2.0
        assert TOLERANCES["center_distance"] == 3.0

    def test_weights_sum(self):
        total = sum(WEIGHTS.values())
        assert abs(total - 1.0) < 0.01

    def test_calculate_param_score_within_tolerance(self):
        score = self.service._calculate_param_score(55, 55, "backset")
        assert score > 0

    def test_calculate_param_score_outside_tolerance(self):
        score = self.service._calculate_param_score(55, 70, "backset")
        assert score == 0

    def test_calculate_param_score_zero_values(self):
        score = self.service._calculate_param_score(0, 55, "backset")
        assert score == 0

    def test_calculate_param_score_none_lock_value(self):
        score = self.service._calculate_param_score(55, None, "backset")
        assert score == 0


class TestLockDTO:
    def test_lock_to_dto(self):
        from app.db.models import Lock, LockTypeEnum
        from app.services.matching_service import MatchingService

        lock = Lock(
            id=1,
            vendor_code="A-001",
            name="Test Lock",
            brand="TestBrand",
            type=LockTypeEnum.embedded,
            backset=55.0,
            center_distance=72.0,
            plate_width=24.0,
            plate_height=235.0,
            plate_thickness=3.0,
            body_width=85.0,
            body_height=165.0,
            body_depth=13.0,
        )

        service = MatchingService()
        dto = service._lock_to_dto(lock)

        assert dto.id == 1
        assert dto.vendor_code == "A-001"
        assert dto.backset == 55.0
        assert dto.type == "embedded"
