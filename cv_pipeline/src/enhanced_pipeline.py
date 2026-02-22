"""
Enhanced Lock Pipeline with YOLO integration
Uses YOLO for detection, then contour analysis for precise measurements
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
import json

from yolo_detector import YOLODetector, YOLODetection
from lock_pipeline import LockContourPipeline, LockFeatures


MODEL_PATH = "runs/detect/lock_train/weights/best.pt"
CONFIDENCE_THRESHOLD = 0.5


@dataclass
class EnhancedLockFeatures:
    yolo_detections: List[YOLODetection]
    contour_features: LockFeatures
    yolo_used: bool


class EnhancedLockPipeline:
    def __init__(self, use_yolo: bool = True, model_path: Optional[str] = None):
        self.use_yolo = use_yolo
        self.model_path = model_path or MODEL_PATH
        self.detector: Optional[YOLODetector] = None
        self.contour_pipeline = LockContourPipeline()
        
        if self.use_yolo:
            self._init_detector()
    
    def _init_detector(self):
        """Initialize YOLO detector."""
        try:
            self.detector = YOLODetector(
                model_path=self.model_path,
                confidence_threshold=CONFIDENCE_THRESHOLD
            )
            print(f"YOLO detector initialized with model: {self.model_path}")
        except Exception as e:
            print(f"Failed to initialize YOLO: {e}")
            print("Falling back to contour-only detection")
            self.use_yolo = False
    
    def analyze(self, image: np.ndarray) -> Dict:
        """
        Main analysis pipeline:
        1. Try YOLO detection first
        2. Use YOLO bbox to crop and refine
        3. Fall back to contour analysis if YOLO fails
        """
        result = {
            'success': False,
            'yolo_used': False,
            'confidence': 0.0,
            'error': None,
            'detections': [],
            'measurements': {}
        }
        
        if self.use_yolo and self.detector:
            detections = self.detector.detect(image)
            result['detections'] = [
                {
                    'class': d.class_name,
                    'confidence': d.confidence,
                    'bbox': d.bbox
                }
                for d in detections
            ]
            
            if detections:
                result['yolo_used'] = True
                
                lock_plate = self._find_detection(detections, 'lock_plate')
                if lock_plate:
                    cropped = self._crop_with_margin(image, lock_plate.bbox, margin=50)
                    contour_result = self.contour_pipeline.analyze_lock(cropped)
                    
                    if contour_result.get('success'):
                        result['success'] = True
                        result['measurements'] = contour_result.get('measurements', {})
                        result['confidence'] = min(
                            lock_plate.confidence + contour_result.get('confidence', 0),
                            1.0
                        )
                        return result
        
        contour_result = self.contour_pipeline.analyze_lock(image)
        result['success'] = contour_result.get('success', False)
        result['measurements'] = contour_result.get('measurements', {})
        result['confidence'] = contour_result.get('confidence', 0.0)
        
        return result
    
    def _find_detection(self, detections: List[YOLODetection], class_name: str) -> Optional[YOLODetection]:
        """Find detection by class name."""
        matches = [d for d in detections if d.class_name == class_name]
        if not matches:
            return None
        return max(matches, key=lambda d: d.confidence)
    
    def _crop_with_margin(self, image: np.ndarray, bbox: Tuple[int, int, int, int], margin: int = 20) -> np.ndarray:
        """Crop image to bbox with margin."""
        x, y, w, h = bbox
        h_img, w_img = image.shape[:2]
        
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(w_img, x + w + margin)
        y2 = min(h_img, y + h + margin)
        
        return image[y1:y2, x1:x2]


def process_image(image_path: str, use_yolo: bool = True, output_path: Optional[str] = None) -> Dict:
    """Process a lock image and return measurements."""
    image = cv2.imread(image_path)
    
    if image is None:
        return {
            'success': False,
            'error': f'Failed to load image: {image_path}',
            'confidence': 0.0
        }
    
    pipeline = EnhancedLockPipeline(use_yolo=use_yolo)
    result = pipeline.analyze(image)
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Result saved to {output_path}")
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_pipeline.py <image_path> [--no-yolo] [output_json_path]")
        print("  --no-yolo: Use only contour detection (no YOLO)")
        sys.exit(1)
    
    use_yolo = "--no-yolo" not in sys.argv
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = process_image(image_path, use_yolo=use_yolo, output_path=output_path)
    print(json.dumps(result, indent=2, default=str))
