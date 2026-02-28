import cv2
import numpy as np
from typing import Optional, Tuple, List


class GeometryCalculator:
    DIN_CYLINDER_WIDTH = 10.0
    DIN_CYLINDER_HEIGHT = 33.0
    DIN_TOP_DIAMETER = 17.0
    BACKSET_TOLERANCE = 2.0
    CENTER_DISTANCE_TOLERANCE = 3.0

    def __init__(self, scale_factor: float):
        self.scale_factor = scale_factor

    def pixels_to_mm(self, pixels: float) -> float:
        return pixels / self.scale_factor

    def mm_to_pixels(self, mm: float) -> float:
        return mm * self.scale_factor

    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        px_distance = np.sqrt(
            (point1[0] - point2[0])**2 +
            (point1[1] - point2[1])**2
        )
        return self.pixels_to_mm(px_distance)

    def calculate_backset(
        self,
        cylinder_center: Tuple[float, float],
        handle_square_center: Tuple[float, float]
    ) -> float:
        return self.calculate_distance(cylinder_center, handle_square_center)

    def calculate_center_distance(
        self,
        cylinder_center: Tuple[float, float],
        handle_center: Tuple[float, float]
    ) -> float:
        return self.calculate_distance(cylinder_center, handle_center)

    def calculate_dimensions(self, bounding_box: Tuple[int, int, int, int]) -> dict:
        x, y, w, h = bounding_box
        return {
            'width': self.pixels_to_mm(w),
            'height': self.pixels_to_mm(h),
        }

    def calculate_hole_diameter(self, contour_points: np.ndarray) -> float:
        x, y, w, h = cv2.boundingRect(contour_points)
        return self.pixels_to_mm(max(w, h))

    def estimate_thickness(self, contour: np.ndarray, image_shape: tuple) -> float:
        if contour is None or len(contour) == 0:
            return 3.0
        
        area = cv2.contourArea(contour)
        if area <= 0:
            return 3.0
        
        x, y, w, h = cv2.boundingRect(contour)
        if w <= 0 or h <= 0:
            return 3.0
        
        bbox_area = w * h
        fill_ratio = area / bbox_area if bbox_area > 0 else 0
        
        estimated_thickness = 3.0 * fill_ratio
        return max(1.0, min(5.0, estimated_thickness))

    def calculate_plate_dimensions(
        self,
        contour_points: np.ndarray
    ) -> dict:
        x, y, w, h = cv2.boundingRect(contour_points)
        return {
            'width_mm': self.pixels_to_mm(w),
            'height_mm': self.pixels_to_mm(h),
        }

    def is_within_tolerance(
        self,
        measured: float,
        expected: float,
        tolerance: float
    ) -> bool:
        return abs(measured - expected) <= tolerance


class LockMeasurementResult:
    def __init__(self):
        self.scale_factor: float = 0.0
        self.plate_width_mm: float = 0.0
        self.plate_height_mm: float = 0.0
        self.backset_mm: float = 0.0
        self.center_distance_mm: float = 0.0
        self.cylinder_hole_center: Optional[Tuple[float, float]] = None
        self.handle_square_center: Optional[Tuple[float, float]] = None
        self.handle_square_size_mm: float = 0.0
        self.mounting_holes: list = []
        self.confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            'scale_factor': self.scale_factor,
            'plate_width_mm': self.plate_width_mm,
            'plate_height_mm': self.plate_height_mm,
            'backset_mm': self.backset_mm,
            'center_distance_mm': self.center_distance_mm,
            'cylinder_hole_center': self.cylinder_hole_center,
            'handle_square_center': self.handle_square_center,
            'handle_square_size_mm': self.handle_square_size_mm,
            'mounting_holes': self.mounting_holes,
            'confidence': self.confidence,
        }


class MeasurementPipeline:
    MIN_SCALE_FACTOR = 5.0
    MAX_SCALE_FACTOR = 50.0
    
    def __init__(self, din_marker_width_mm: float = 10.0):
        self.din_marker_width_mm = din_marker_width_mm

    def process(
        self,
        image: np.ndarray,
        marker_bounding_box: Tuple[int, int, int, int]
    ) -> dict:
        marker_x, marker_y, marker_w, marker_h = marker_bounding_box
        
        slot_width_px = min(marker_w, marker_h)
        full_height_px = max(marker_w, marker_h)
        
        aspect = full_height_px / slot_width_px
        if not (1.5 <= aspect <= 4.0):
            raise ValueError(f"Invalid cylinder aspect ratio: {aspect:.2f}")
        
        scale_factor = slot_width_px / self.din_marker_width_mm
        
        if not (self.MIN_SCALE_FACTOR <= scale_factor <= self.MAX_SCALE_FACTOR):
            raise ValueError(f"Unrealistic scale factor: {scale_factor:.2f}")

        from contour_analyzer import ContourAnalyzer
        from edge_detector import EdgeDetector

        edge_detector = EdgeDetector()
        gray = edge_detector.to_grayscale(image)
        blurred = edge_detector.gaussian_blur(gray, sigma=1.5)
        edges = edge_detector.canny_edge_detection(blurred, threshold1=50, threshold2=150)
        
        contours_external = edge_detector.find_contours_external(edges)

        contour_analyzer = ContourAnalyzer(min_area=50, max_area=100000)
        contours = contour_analyzer.find_contours(edges)

        plate_contour = contour_analyzer.find_plate_contour(contours)
        handle_square = contour_analyzer.find_handle_square(contours, scale_factor)
        mounting_holes = contour_analyzer.find_mounting_holes(contours, scale_factor)
        cylinder_hole = contour_analyzer.find_cylinder_hole(contours, plate_contour)

        geometry_calc = GeometryCalculator(scale_factor)

        result = LockMeasurementResult()
        result.scale_factor = scale_factor

        if plate_contour:
            dims = geometry_calc.calculate_plate_dimensions(plate_contour.points)
            result.plate_width_mm = dims['width_mm']
            result.plate_height_mm = dims['height_mm']

        if handle_square:
            result.handle_square_center = handle_square.center
            result.handle_square_size_mm = geometry_calc.pixels_to_mm(
                max(handle_square.bounding_box[2], handle_square.bounding_box[3])
            )

        if cylinder_hole:
            result.cylinder_hole_center = cylinder_hole.center

        if result.cylinder_hole_center and result.handle_square_center:
            result.backset_mm = geometry_calc.calculate_backset(
                result.cylinder_hole_center,
                result.handle_square_center
            )

        if len(result.mounting_holes) >= 2:
            holes = sorted(result.mounting_holes, key=lambda h: h.get('y', 0))
            h1, h2 = holes[0], holes[1]
            dy = h2.get('y', 0) - h1.get('y', 0)
            dx = h2.get('x', 0) - h1.get('x', 0)
            result.center_distance_mm = (dx**2 + dy**2) ** 0.5
        elif result.cylinder_hole_center and result.handle_square_center:
            result.center_distance_mm = result.backset_mm

        for hole in mounting_holes:
            result.mounting_holes.append({
                'x': geometry_calc.pixels_to_mm(hole.center[0]),
                'y': geometry_calc.pixels_to_mm(hole.center[1]),
                'diameter': geometry_calc.calculate_hole_diameter(hole.points),
            })

        result.confidence = self._calculate_confidence(result)

        return result.to_dict()

    def _calculate_confidence(self, result: LockMeasurementResult) -> float:
        confidence = 0.0

        if result.plate_width_mm > 20:
            confidence += 0.15
        if result.plate_height_mm > 80:
            confidence += 0.15
        if result.cylinder_hole_center is not None:
            confidence += 0.25
        if result.handle_square_center is not None:
            confidence += 0.20
        if len(result.mounting_holes) >= 2:
            confidence += 0.15
        if result.backset_mm > 0:
            confidence += 0.10

        return min(confidence, 1.0)


from typing import Tuple
