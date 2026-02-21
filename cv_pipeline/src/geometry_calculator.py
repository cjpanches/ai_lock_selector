import numpy as np

class GeometryCalculator:
    DIN_CYLINDER_WIDTH = 10.0
    DIN_CYLINDER_HEIGHT = 17.0
    
    def __init__(self, scale_factor: float):
        self.scale_factor = scale_factor
    
    def pixels_to_mm(self, pixels: float) -> float:
        return pixels / self.scale_factor
    
    def mm_to_pixels(self, mm: float) -> float:
        return mm * self.scale_factor
    
    def calculate_backset(
        self, 
        cylinder_center: tuple, 
        handle_square_center: tuple
    ) -> float:
        px_distance = np.sqrt(
            (cylinder_center[0] - handle_square_center[0])**2 +
            (cylinder_center[1] - handle_square_center[1])**2
        )
        return self.pixels_to_mm(px_distance)
    
    def calculate_center_distance(
        self,
        cylinder_center: tuple,
        handle_center: tuple
    ) -> float:
        return self.calculate_backset(cylinder_center, handle_center)
    
    def calculate_dimensions(self, bounding_box: tuple) -> dict:
        x, y, w, h = bounding_box
        return {
            'width': self.pixels_to_mm(w),
            'height': self.pixels_to_mm(h),
        }
    
    def calculate_hole_diameter(self, contour_points: np.ndarray) -> float:
        x, y, w, h = cv2.boundingRect(contour_points)
        return self.pixels_to_mm((w + h) / 2)
    
    def estimate_thickness(self, contour: np.ndarray, image_shape: tuple) -> float:
        return 3.0

import cv2

class MeasurementPipeline:
    def __init__(self, din_marker_width_mm: float = 10.0):
        self.din_marker_width_mm = din_marker_width_mm
    
    def process(self, image: np.ndarray, marker_bounding_box: tuple) -> dict:
        marker_x, marker_y, marker_w, marker_h = marker_bounding_box
        
        scale_factor = marker_w / self.din_marker_width_mm
        
        from contour_analyzer import ContourAnalyzer
        from edge_detector import EdgeDetector
        
        edge_detector = EdgeDetector()
        gray = edge_detector.to_grayscale(image)
        edges = edge_detector.canny_edge_detection(gray)
        
        contour_analyzer = ContourAnalyzer()
        contours = contour_analyzer.find_contours(edges)
        
        plate_contour = contour_analyzer.find_plate_contour(contours)
        handle_square = contour_analyzer.find_handle_square(contours)
        mounting_holes = contour_analyzer.find_circular_holes(contours)
        
        geometry_calc = GeometryCalculator(scale_factor)
        
        result = {
            'scale_factor': scale_factor,
            'dimensions': {},
            'mounting_holes': [],
            'handle_square': None,
            'confidence': 0.5,
        }
        
        if plate_contour:
            result['dimensions'] = geometry_calc.calculate_dimensions(plate_contour.bounding_box)
        
        if handle_square:
            result['handle_square'] = {
                'x': geometry_calc.pixels_to_mm(handle_square.center[0]),
                'y': geometry_calc.pixels_to_mm(handle_square.center[1]),
                'size': geometry_calc.pixels_to_mm(handle_square.bounding_box[2]),
            }
        
        for hole in mounting_holes:
            result['mounting_holes'].append({
                'x': geometry_calc.pixels_to_mm(hole.center[0]),
                'y': geometry_calc.pixels_to_mm(hole.center[1]),
                'diameter': geometry_calc.pixels_to_mm(hole.bounding_box[2]),
            })
        
        result['confidence'] = self._calculate_confidence(result)
        
        return result
    
    def _calculate_confidence(self, result: dict) -> float:
        confidence = 0.4
        
        if len(result['mounting_holes']) >= 2:
            confidence += 0.2
        
        if result['handle_square'] is not None:
            confidence += 0.2
        
        if result['dimensions'].get('width', 0) > 20:
            confidence += 0.1
        
        if result['dimensions'].get('height', 0) > 100:
            confidence += 0.1
        
        return min(confidence, 1.0)
