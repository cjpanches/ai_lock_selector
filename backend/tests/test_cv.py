import pytest
import numpy as np
import sys
from pathlib import Path

cv_path = Path(__file__).parent.parent.parent / "cv_pipeline" / "src"
sys.path.insert(0, str(cv_path))


class TestGeometryCalculator:
    def test_pixels_to_mm(self):
        from geometry_calculator import GeometryCalculator

        calc = GeometryCalculator(scale_factor=10.0)
        result = calc.pixels_to_mm(100)
        assert result == 10.0

    def test_mm_to_pixels(self):
        from geometry_calculator import GeometryCalculator

        calc = GeometryCalculator(scale_factor=10.0)
        result = calc.mm_to_pixels(10.0)
        assert result == 100.0

    def test_calculate_distance(self):
        from geometry_calculator import GeometryCalculator

        calc = GeometryCalculator(scale_factor=10.0)
        result = calc.calculate_distance((0, 0), (100, 0))
        assert result == 10.0

    def test_is_within_tolerance(self):
        from geometry_calculator import GeometryCalculator

        calc = GeometryCalculator(scale_factor=10.0)
        assert calc.is_within_tolerance(55, 55, 2) == True
        assert calc.is_within_tolerance(55, 57, 2) == True
        assert calc.is_within_tolerance(55, 58, 2) == False


class TestEdgeDetector:
    def test_to_grayscale(self):
        from edge_detector import EdgeDetector

        img = np.zeros((100, 100, 3), dtype=np.uint8)
        gray = EdgeDetector.to_grayscale(img)
        assert len(gray.shape) == 2

    def test_gaussian_blur(self):
        from edge_detector import EdgeDetector

        img = np.zeros((100, 100), dtype=np.uint8)
        blurred = EdgeDetector.gaussian_blur(img)
        assert blurred.shape == img.shape


class TestContourAnalyzer:
    def test_contour_result_creation(self):
        from contour_analyzer import ContourResult

        result = ContourResult(
            points=np.array([[0, 0], [10, 0], [10, 10], [0, 10]]),
            bounding_box=(0, 0, 10, 10),
            area=100,
            perimeter=40,
            center=(5, 5),
        )
        assert result.area == 100
        assert result.center == (5, 5)
