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

    def test_find_circular_holes(self):
        from contour_analyzer import ContourAnalyzer, ContourResult
        
        analyzer = ContourAnalyzer()
        
        circle_contour = ContourResult(
            points=np.array([]),
            bounding_box=(0, 0, 20, 20),
            area=314,
            perimeter=62.8,
            center=(10, 10),
            circularity=0.9,
            aspect_ratio=1.0
        )
        
        results = analyzer.find_circular_holes([circle_contour], min_diameter_pixels=10, max_diameter_pixels=50)
        assert len(results) == 1

    def test_find_din_cylinder_hole(self):
        from contour_analyzer import ContourAnalyzer, ContourResult
        
        analyzer = ContourAnalyzer()
        
        din_contour = ContourResult(
            points=np.array([]),
            bounding_box=(0, 0, 20, 34),
            area=680,
            perimeter=108,
            center=(10, 17),
            circularity=0.3,
            aspect_ratio=0.59
        )
        
        scale_factor = 2.0
        result = analyzer.find_din_cylinder_hole([din_contour], scale_factor, tolerance=0.5)
        assert result is not None

    def test_find_mounting_holes(self):
        from contour_analyzer import ContourAnalyzer, ContourResult
        
        analyzer = ContourAnalyzer()
        
        hole_contour = ContourResult(
            points=np.array([]),
            bounding_box=(0, 0, 14, 14),
            area=150,
            perimeter=50,
            center=(7, 7),
            circularity=0.75,
            aspect_ratio=1.0
        )
        
        scale_factor = 2.0
        results = analyzer.find_mounting_holes([hole_contour], scale_factor, expected_count=2)
        assert len(results) >= 1


class TestLockPipeline:
    def test_lock_features_dataclass(self):
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cv_pipeline" / "src"))
        from lock_pipeline import LockFeatures
        
        features = LockFeatures()
        assert features.mounting_holes == []
        
        features.mounting_holes.append(np.array([[0, 0]]))
        assert len(features.mounting_holes) == 1

    def test_scale_factor_calculation(self):
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cv_pipeline" / "src"))
        from lock_pipeline import LockContourPipeline
        
        pipeline = LockContourPipeline()
        
        marker_bbox = (0, 0, 100, 330)
        scale = pipeline.calculate_scale_factor(marker_bbox)
        assert scale == 10.0
        
        marker_bbox_obb = (0, 0, 100, 330, 0)
        scale_obb = pipeline.calculate_scale_factor(marker_bbox_obb)
        assert scale_obb == 10.0
