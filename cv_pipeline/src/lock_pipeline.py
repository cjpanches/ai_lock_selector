import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
import json


@dataclass
class LockFeatures:
    plate_contour: Optional[np.ndarray] = None
    plate_bbox: Optional[Tuple[int, int, int, int]] = None
    plate_dimensions_mm: Optional[Tuple[float, float]] = None
    
    cylinder_hole: Optional[np.ndarray] = None
    cylinder_center_px: Optional[Tuple[float, float]] = None
    
    handle_square: Optional[np.ndarray] = None
    handle_center_px: Optional[Tuple[float, float]] = None
    handle_size_mm: float = 0.0
    
    mounting_holes: List[np.ndarray] = None
    
    def __post_init__(self):
        if self.mounting_holes is None:
            self.mounting_holes = []


class LockContourPipeline:
    DIN_CYLINDER_WIDTH = 10.0
    DIN_CYLINDER_HEIGHT = 33.0
    DIN_TOP_DIAMETER = 17.0
    
    PLATE_MIN_HEIGHT_MM = 200
    PLATE_MAX_HEIGHT_MM = 400
    PLATE_MIN_WIDTH_MM = 20
    PLATE_MAX_WIDTH_MM = 50
    
    MOUNTING_HOLE_DIAMETER_MM = (4.0, 7.0)
    HANDLE_SQUARE_SIZE_MM = (7.0, 10.0)
    
    MIN_SCALE_FACTOR = 5.0
    MAX_SCALE_FACTOR = 50.0
    VALID_ASPECT_RATIO_RANGE = (1.5, 4.0)

    def __init__(self):
        self.scale_factor: float = 0.0

    def detect_marker(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        marker_candidates = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            
            if area < 100:
                continue
            
            aspect_ratio = w / h if h > 0 else 0
            if 0.3 < aspect_ratio < 0.8:
                marker_candidates.append((x, y, w, h, area))
        
        if marker_candidates:
            marker_candidates.sort(key=lambda x: x[4], reverse=True)
            x, y, w, h, _ = marker_candidates[0]
            return (x, y, w, h)
        
        return None

    def calculate_scale_factor(self, marker_bbox: Tuple[int, int, int, int], mask_roi: Optional[np.ndarray] = None) -> float:
        """
        Calculate scale factor using the 10mm slot width of Euro cylinder.
        
        Args:
            marker_bbox: YOLO detection bbox (x, y, w, h) or OBB (x,y,w,h,angle)
            mask_roi: Optional binary mask of detected cylinder for precise measurement
        
        Returns:
            float: pixels_per_mm scale factor
        
        Raises:
            ValueError: If detection is invalid or scale cannot be calculated
        """
        if len(marker_bbox) == 5:
            x, y, w, h, angle = marker_bbox
        else:
            x, y, w, h = marker_bbox
        
        if w <= 0 or h <= 0:
            raise ValueError(f"Invalid bbox dimensions: w={w}, h={h}")
        
        slot_width_px = min(w, h)
        full_height_px = max(w, h)
        
        aspect = full_height_px / slot_width_px if slot_width_px > 0 else 0
        
        if not (self.VALID_ASPECT_RATIO_RANGE[0] <= aspect <= self.VALID_ASPECT_RATIO_RANGE[1]):
            raise ValueError(f"Invalid cylinder aspect ratio: {aspect:.2f}, expected {self.VALID_ASPECT_RATIO_RANGE}")
        
        scale_factor = slot_width_px / self.DIN_CYLINDER_WIDTH
        
        if not (self.MIN_SCALE_FACTOR <= scale_factor <= self.MAX_SCALE_FACTOR):
            raise ValueError(f"Unrealistic scale factor: {scale_factor:.2f} px/mm, expected {self.MIN_SCALE_FACTOR}-{self.MAX_SCALE_FACTOR}")
        
        return scale_factor
    
    def _calculate_scale_from_mask(self, mask_roi: np.ndarray) -> float:
        """
        Precise measurement of slot width from binary mask.
        Measures width at multiple heights and takes minimum (narrowest point = slot).
        """
        h, w = mask_roi.shape[:2]
        
        widths = []
        center_region = mask_roi[int(h*0.3):int(h*0.7), :]
        
        for y in range(center_region.shape[0]):
            row = center_region[y, :]
            white_pixels = np.where(row > 127)[0]
            if len(white_pixels) > 0:
                width = white_pixels[-1] - white_pixels[0]
                widths.append(width)
        
        if not widths:
            raise ValueError("Cannot measure width from mask")
        
        slot_width_px = min(widths)
        return slot_width_px / self.DIN_CYLINDER_WIDTH

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        return blurred

    def detect_edges(self, preprocessed: np.ndarray) -> np.ndarray:
        edges = cv2.Canny(preprocessed, 50, 150)
        
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        return dilated

    def find_all_contours(self, edges: np.ndarray) -> List[Tuple[np.ndarray, str]]:
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if hierarchy is None:
            return []
        
        results = []
        for i, contour in enumerate(contours):
            h = hierarchy[0][i]
            contour_type = "external"
            
            if h[3] != -1:
                parent_idx = h[3]
                parent_area = cv2.contourArea(contours[parent_idx]) if parent_idx < len(contours) else 0
                area = cv2.contourArea(contour)
                
                if area < parent_area * 0.5:
                    contour_type = "hole"
                else:
                    contour_type = "child"
            
            results.append((contour, contour_type))
        
        return results

    def is_circular_hole(
        self,
        contour: np.ndarray,
        expected_diameter_mm: Tuple[float, float]
    ) -> bool:
        if self.scale_factor <= 0:
            return False
        
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return False
        
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        
        if circularity < 0.5:
            return False
        
        x, y, w, h = cv2.boundingRect(contour)
        diameter_px = max(w, h)
        diameter_mm = diameter_px / self.scale_factor
        
        return expected_diameter_mm[0] <= diameter_mm <= expected_diameter_mm[1]

    def is_rectangular_hole(
        self,
        contour: np.ndarray,
        expected_size_mm: Tuple[float, float],
        tolerance: float = 0.5
    ) -> bool:
        if self.scale_factor <= 0:
            return False
        
        x, y, w, h = cv2.boundingRect(contour)
        
        width_mm = w / self.scale_factor
        height_mm = h / self.scale_factor
        
        min_size, max_size = expected_size_mm
        
        width_ok = (min_size * (1 - tolerance)) <= width_mm <= (max_size * (1 + tolerance))
        height_ok = (min_size * (1 - tolerance)) <= height_mm <= (max_size * (1 + tolerance))
        
        area = cv2.contourArea(contour)
        bbox_area = w * h
        fill_ratio = area / bbox_area if bbox_area > 0 else 0
        
        return (width_ok or height_ok) and fill_ratio > 0.5

    def analyze_lock(self, image: np.ndarray) -> Dict:
        marker_bbox = self.detect_marker(image)
        
        if marker_bbox is None:
            return {
                'success': False,
                'error': 'Marker not found',
                'confidence': 0.0
            }
        
        self.scale_factor = self.calculate_scale_factor(marker_bbox)
        
        preprocessed = self.preprocess_image(image)
        edges = self.detect_edges(preprocessed)
        
        contours_data = self.find_all_contours(edges)
        
        features = LockFeatures()
        
        plate_contours = []
        hole_contours = []
        
        for contour, contour_type in contours_data:
            area = cv2.contourArea(contour)
            if area < 50:
                continue
            
            if contour_type == "external" or contour_type == "child":
                plate_contours.append(contour)
            else:
                hole_contours.append(contour)
        
        if plate_contours:
            best_plate = max(plate_contours, key=cv2.contourArea)
            features.plate_contour = best_plate
            features.plate_bbox = cv2.boundingRect(best_plate)
            
            x, y, w, h = features.plate_bbox
            features.plate_dimensions_mm = (
                w / self.scale_factor,
                h / self.scale_factor
            )
        
        for hole_contour in hole_contours:
            if self.is_circular_hole(hole_contour, self.MOUNTING_HOLE_DIAMETER_MM):
                features.mounting_holes.append(hole_contour)
            
            if self.is_rectangular_hole(hole_contour, (self.DIN_CYLINDER_WIDTH, self.DIN_CYLINDER_HEIGHT), 0.6):
                features.cylinder_hole = hole_contour
                M = cv2.moments(hole_contour)
                if M["m00"] != 0:
                    features.cylinder_center_px = (
                        M["m10"] / M["m00"],
                        M["m01"] / M["m00"]
                    )
            
            if self.is_rectangular_hole(hole_contour, self.HANDLE_SQUARE_SIZE_MM, 0.5):
                features.handle_square = hole_contour
                M = cv2.moments(hole_contour)
                if M["m00"] != 0:
                    features.handle_center_px = (
                        M["m10"] / M["m00"],
                        M["m01"] / M["m00"]
                    )
                    x, y, w, h = cv2.boundingRect(hole_contour)
                    features.handle_size_mm = max(w, h) / self.scale_factor
        
        result = self.build_result(features)
        
        return result

    def build_result(self, features: LockFeatures) -> Dict:
        result = {
            'success': True,
            'confidence': 0.0,
            'scale_factor': self.scale_factor,
            'plate': {},
            'cylinder': {},
            'handle': {},
            'mounting_holes': [],
            'measurements': {}
        }
        
        confidence = 0.0
        
        if features.plate_dimensions_mm:
            w, h = features.plate_dimensions_mm
            result['plate'] = {
                'width_mm': round(w, 1),
                'height_mm': round(h, 1)
            }
            if self.PLATE_MIN_WIDTH_MM <= w <= self.PLATE_MAX_WIDTH_MM:
                confidence += 0.2
            if self.PLATE_MIN_HEIGHT_MM <= h <= self.PLATE_MAX_HEIGHT_MM:
                confidence += 0.2
        
        if features.cylinder_center_px:
            cx, cy = features.cylinder_center_px
            result['cylinder'] = {
                'x_px': round(cx, 1),
                'y_px': round(cy, 1),
                'x_mm': round(cx / self.scale_factor, 1),
                'y_mm': round(cy / self.scale_factor, 1)
            }
            confidence += 0.2
        
        if features.handle_center_px:
            hx, hy = features.handle_center_px
            result['handle'] = {
                'x_px': round(hx, 1),
                'y_px': round(hy, 1),
                'x_mm': round(hx / self.scale_factor, 1),
                'y_mm': round(hy / self.scale_factor, 1),
                'size_mm': round(features.handle_size_mm, 1)
            }
            confidence += 0.15
            
            if features.cylinder_center_px:
                backset = np.sqrt(
                    (features.cylinder_center_px[0] - hx)**2 +
                    (features.cylinder_center_px[1] - hy)**2
                ) / self.scale_factor
                result['measurements']['backset_mm'] = round(backset, 1)
                result['measurements']['center_distance_mm'] = round(backset, 1)
                confidence += 0.15
        
        for i, hole in enumerate(features.mounting_holes[:3]):
            M = cv2.moments(hole)
            if M["m00"] != 0:
                hx = M["m10"] / M["m00"]
                hy = M["m01"] / M["m00"]
                x, y, w, h = cv2.boundingRect(hole)
                diameter_mm = max(w, h) / self.scale_factor
                
                result['mounting_holes'].append({
                    'index': i + 1,
                    'x_mm': round(hx / self.scale_factor, 1),
                    'y_mm': round(hy / self.scale_factor, 1),
                    'diameter_mm': round(diameter_mm, 1)
                })
        
        if len(features.mounting_holes) >= 2:
            confidence += 0.1
        
        result['confidence'] = min(confidence, 1.0)
        
        return result


def process_lock_image(image_path: str, output_path: Optional[str] = None) -> Dict:
    image = cv2.imread(image_path)
    
    if image is None:
        return {
            'success': False,
            'error': f'Failed to load image: {image_path}',
            'confidence': 0.0
        }
    
    pipeline = LockContourPipeline()
    result = pipeline.analyze_lock(image)
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Result saved to {output_path}")
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lock_pipeline.py <image_path> [output_json_path]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = process_lock_image(image_path, output_path)
    print(json.dumps(result, indent=2))
