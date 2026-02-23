import base64
import io
from PIL import Image
import numpy as np
import cv2
from datetime import datetime
from app.models.schemas import LockProfileDTO, LockDimensionsDTO, MountingHoleDTO

class MeasurementService:
    def __init__(self):
        self.din_cylinder_width = 10.0
        self.din_cylinder_height = 17.0
    
    async def process_measurement(
        self,
        image_base64: str,
        scale_factor: float,
        marker_x: float = None,
        marker_y: float = None,
    ) -> LockProfileDTO:
        """Обработка изображения и измерение параметров замка"""
        
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
            edges = cv2.Canny(blurred, 50, 150)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            dimensions = await self._calculate_dimensions(
                contours, 
                scale_factor,
                cylinder_hole=cylinder_hole,
                handle_square=handle_square,
                mounting_holes=mounting_holes
            )
            mounting_holes = await self._find_mounting_holes(contours, scale_factor)
            handle_square = await self._find_handle_square(contours, scale_factor)
            cylinder_hole = await self._find_cylinder_hole(contours, scale_factor, marker_x, marker_y)
            
            confidence = self._calculate_confidence(dimensions, mounting_holes, handle_square)
            
            return LockProfileDTO(
                dimensions=LockDimensionsDTO(**dimensions),
                mounting_holes=[MountingHoleDTO(**h) for h in mounting_holes],
                handle_square=handle_square,
                cylinder_hole=cylinder_hole,
                confidence=confidence,
                captured_at=datetime.now().isoformat(),
            )
            
        except Exception as e:
            raise Exception(f"Measurement failed: {str(e)}")
    
    async def _calculate_dimensions(self, contours, scale_factor, cylinder_hole=None, handle_square=None, mounting_holes=None):
        """Вычисление размеров замка"""
        
        plate_contour = self._find_plate_contour(contours)
        
        if plate_contour is None:
            return {
                "backset": 0,
                "center_distance": 0,
                "plate_width": 0,
                "plate_height": 0,
                "plate_thickness": 3.0,
                "body_width": 0,
                "body_height": 0,
                "body_depth": 0,
            }
        
        x, y, w, h = cv2.boundingRect(plate_contour)
        
        plate_width = (w / scale_factor)
        plate_height = (h / scale_factor)
        
        backset = 0.0
        center_distance = 0.0
        
        if cylinder_hole and handle_square:
            dx = handle_square.get('x', 0) - cylinder_hole.get('x', 0)
            dy = handle_square.get('y', 0) - cylinder_hole.get('y', 0)
            backset = (dx**2 + dy**2) ** 0.5
        
        if mounting_holes and len(mounting_holes) >= 2:
            sorted_holes = sorted(mounting_holes, key=lambda h: h.get('y', 0))
            h1, h2 = sorted_holes[0], sorted_holes[1]
            dx = h2.get('x', 0) - h1.get('x', 0)
            dy = h2.get('y', 0) - h1.get('y', 0)
            center_distance = (dx**2 + dy**2) ** 0.5
        elif cylinder_hole and handle_square:
            center_distance = backset
        
        return {
            "backset": backset if backset > 0 else 55.0,
            "center_distance": center_distance if center_distance > 0 else 72.0,
            "plate_width": plate_width,
            "plate_height": plate_height,
            "plate_thickness": 3.0,
            "body_width": plate_width,
            "body_height": plate_height * 1.5,
            "body_depth": 0,
        }
    
    def _find_plate_contour(self, contours):
        """Поиск контура планки замка"""
        if not contours:
            return None
        
        best_contour = None
        best_score = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                
                if 0.1 < aspect_ratio < 1.0:
                    score = area * (1 - abs(aspect_ratio - 0.3))
                    if score > best_score:
                        best_score = score
                        best_contour = contour
        
        return best_contour
    
    async def _find_mounting_holes(self, contours, scale_factor):
        """Поиск крепёжных отверстий"""
        holes = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 100 < area < 2000:
                perimeter = cv2.arcLength(contour, True)
                circularity = (4 * np.pi * area) / (perimeter * perimeter) if perimeter > 0 else 0
                
                if circularity > 0.7:
                    x, y, w, h = cv2.boundingRect(contour)
                    diameter = (w + h) / 2 / scale_factor
                    
                    if 6 <= diameter <= 12:
                        holes.append({
                            "x": x / scale_factor,
                            "y": y / scale_factor,
                            "diameter": diameter,
                        })
        
        return holes
    
    async def _find_handle_square(self, contours, scale_factor):
        """Поиск квадрата ручки"""
        for contour in contours:
            area = cv2.contourArea(contour)
            if 200 < area < 1500:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                
                if 0.7 < aspect_ratio < 1.3:
                    return {
                        "x": x / scale_factor,
                        "y": y / scale_factor,
                        "size": w / scale_factor,
                    }
        
        return None
    
    async def _find_cylinder_hole(self, contours, scale_factor, marker_x=None, marker_y=None):
        """Поиск отверстия цилиндра"""
        if marker_x and marker_y:
            return {
                "x": marker_x,
                "y": marker_y,
                "width": self.din_cylinder_width,
                "height": self.din_cylinder_height,
            }
        
        return None
    
    def _calculate_confidence(self, dimensions, mounting_holes, handle_square):
        """Расчёт достоверности измерений"""
        confidence = 0.4
        
        if len(mounting_holes) >= 2:
            confidence += 0.2
        
        if handle_square is not None:
            confidence += 0.2
        
        dims = dimensions
        if dims["backset"] > 0 and dims["backset"] < 100:
            confidence += 0.1
        
        if dims["plate_width"] > 20 and dims["plate_width"] < 50:
            confidence += 0.1
        
        return min(confidence, 1.0)
