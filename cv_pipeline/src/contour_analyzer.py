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
    circularity: float = 0.0
    aspect_ratio: float = 0.0


class ContourAnalyzer:
    DIN_CYLINDER_SIZE = (10.0, 17.0)
    MOUNTING_HOLE_DIAMETER_RANGE = (4.0, 8.0)
    HANDLE_SQUARE_SIZE_RANGE = (7.0, 10.0)

    def __init__(self, min_area: int = 100, max_area: int = 50000):
        self.min_area = min_area
        self.max_area = max_area

    def find_contours(self, edges: np.ndarray) -> List[ContourResult]:
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

                circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
                aspect_ratio = w / h if h > 0 else 0

                results.append(ContourResult(
                    points=contour,
                    bounding_box=(x, y, w, h),
                    area=area,
                    perimeter=perimeter,
                    center=(cx, cy),
                    circularity=circularity,
                    aspect_ratio=aspect_ratio,
                ))

        return results

    def find_circular_holes(
        self,
        contours: List[ContourResult],
        min_diameter_pixels: float = 10,
        max_diameter_pixels: float = 50
    ) -> List[ContourResult]:
        holes = []
        for contour in contours:
            area = contour.area
            perimeter = contour.perimeter

            if perimeter == 0:
                continue

            circularity = (4 * np.pi * area) / (perimeter ** 2)

            if circularity > 0.6:
                x, y, w, h = contour.bounding_box
                diameter = max(w, h)

                if min_diameter_pixels <= diameter <= max_diameter_pixels:
                    holes.append(contour)

        return sorted(holes, key=lambda c: c.center[0])
    
    def find_din_cylinder_hole(
        self,
        contours: List[ContourResult],
        scale_factor: float,
        tolerance: float = 0.4
    ) -> Optional[ContourResult]:
        target_width_mm, target_height_mm = self.DIN_CYLINDER_SIZE
        target_width_px = target_width_mm * scale_factor
        target_height_px = target_height_mm * scale_factor

        best_match = None
        best_score = float('inf')

        for contour in contours:
            x, y, w, h = contour.bounding_box

            if w < 5 or h < 5:
                continue

            width_diff = abs(w - target_width_px) / target_width_px
            height_diff = abs(h - target_height_px) / target_height_px

            if width_diff < tolerance and height_diff < tolerance:
                score = width_diff + height_diff
                if score < best_score:
                    best_score = score
                    best_match = contour

        return best_match

    def find_mounting_holes(
        self,
        contours: List[ContourResult],
        scale_factor: float,
        expected_count: int = 2
    ) -> List[ContourResult]:
        min_diameter_mm, max_diameter_mm = self.MOUNTING_HOLE_DIAMETER_RANGE
        min_diameter_px = min_diameter_mm * scale_factor
        max_diameter_px = max_diameter_mm * scale_factor

        mounting_holes = []
        for contour in contours:
            area = contour.area
            perimeter = contour.perimeter

            if perimeter == 0:
                continue

            circularity = (4 * np.pi * area) / (perimeter ** 2)

            if circularity > 0.5:
                x, y, w, h = contour.bounding_box
                diameter = max(w, h)

                if min_diameter_px <= diameter <= max_diameter_px:
                    mounting_holes.append(contour)

        mounting_holes.sort(key=lambda c: c.center[1])
        return mounting_holes[:expected_count] if len(mounting_holes) >= expected_count else mounting_holes

    def find_plate_contour(self, contours: List[ContourResult]) -> Optional[ContourResult]:
        if not contours:
            return None

        candidates = []
        for contour in contours:
            area = contour.area
            x, y, w, h = contour.bounding_box
            aspect_ratio = w / h if h > 0 else 0

            if area < 5000:
                continue

            if 0.15 < aspect_ratio < 0.6:
                score = area * (1 - abs(aspect_ratio - 0.3))
                candidates.append((contour, score))

        if candidates:
            return max(candidates, key=lambda x: x[1])[0]

        if contours:
            return max(contours, key=lambda c: c.area)

        return None

    def find_handle_square(
        self,
        contours: List[ContourResult],
        scale_factor: float
    ) -> Optional[ContourResult]:
        min_size_mm, max_size_mm = self.HANDLE_SQUARE_SIZE_RANGE
        min_size_px = min_size_mm * scale_factor
        max_size_px = max_size_mm * scale_factor

        for contour in contours:
            area = contour.area
            x, y, w, h = contour.bounding_box
            aspect_ratio = w / h if h > 0 else 0
            size = max(w, h)

            if min_size_px <= size <= max_size_px:
                if 0.6 < aspect_ratio < 1.6:
                    return contour

        return None

    def find_cylinder_hole(
        self,
        contours: List[ContourResult],
        plate_contour: Optional[ContourResult] = None
    ) -> Optional[ContourResult]:
        if plate_contour:
            px, py, pw, ph = plate_contour.bounding_box
            plate_center_x = px + pw / 2
            plate_center_y = py + ph / 2

            candidates = []
            for contour in contours:
                cx, cy = contour.center
                if py < cy < py + ph and px < cx < px + pw:
                    distance = abs(cy - py)
                    candidates.append((contour, distance))

            if candidates:
                return min(candidates, key=lambda x: x[1])[0]

        for contour in contours:
            if 0.3 < contour.aspect_ratio < 1.0:
                return contour

        return None
