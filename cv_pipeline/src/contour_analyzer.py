import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class ContourResult:
    points: np.ndarray
    bounding_box: Tuple[int, int, int, int]
    area: float
    perimeter: float
    center: Tuple[float, float]

class ContourAnalyzer:
    def __init__(self, min_area: int = 100, max_area: int = 50000):
        self.min_area = min_area
        self.max_area = max_area
    
    def find_contours(self, edges: np.ndarray) -> List[ContourResult]:
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        results = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area <= area <= self.max_area:
                perimeter = cv2.arcLength(contour, True)
                x, y, w, h = cv2.boundingRect(contour)
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = M["m10"] / M["m00"]
                    cy = M["m01"] / M["m00"]
                else:
                    cx, cy = x + w/2, y + h/2
                
                results.append(ContourResult(
                    points=contour,
                    bounding_box=(x, y, w, h),
                    area=area,
                    perimeter=perimeter,
                    center=(cx, cy),
                ))
        
        return results
    
    def find_circular_holes(self, contours: List[ContourResult], min_diameter: float = 5, max_diameter: float = 15) -> List[ContourResult]:
        holes = []
        for contour in contours:
            area = contour.area
            perimeter = contour.perimeter
            
            if perimeter == 0:
                continue
                
            circularity = (4 * np.pi * area) / (perimeter ** 2)
            
            if circularity > 0.7:
                x, y, w, h = contour.bounding_box
                diameter = (w + h) / 2
                
                if min_diameter <= diameter <= max_diameter:
                    holes.append(contour)
        
        return holes
    
    def find_plate_contour(self, contours: List[ContourResult]) -> Optional[ContourResult]:
        if not contours:
            return None
        
        best_contour = None
        best_score = 0
        
        for contour in contours:
            x, y, w, h = contour.bounding_box
            aspect_ratio = w / h if h > 0 else 0
            
            if 0.1 < aspect_ratio < 1.0:
                score = contour.area * (1 - abs(aspect_ratio - 0.3))
                if score > best_score:
                    best_score = score
                    best_contour = contour
        
        return best_contour
    
    def find_handle_square(self, contours: List[ContourResult]) -> Optional[ContourResult]:
        for contour in contours:
            area = contour.area
            
            if 200 < area < 1500:
                x, y, w, h = contour.bounding_box
                aspect_ratio = w / h if h > 0 else 0
                
                if 0.7 < aspect_ratio < 1.3:
                    return contour
        
        return None
