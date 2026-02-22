import base64
import sys
import os
from pathlib import Path
import numpy as np
import cv2
from typing import Optional, Dict

cv_pipeline_path = Path(__file__).parent.parent / "cv_pipeline" / "src"
if cv_pipeline_path.exists():
    sys.path.insert(0, str(cv_pipeline_path))

try:
    from yolo_detector import YOLODetector
    from lock_pipeline import LockContourPipeline
except ImportError:
    YOLODetector = None
    LockContourPipeline = None


class CVService:
    def __init__(self):
        if YOLODetector:
            try:
                self.yolo_detector = YOLODetector()
            except Exception as e:
                print(f"YOLO init failed: {e}")
                self.yolo_detector = None
        else:
            self.yolo_detector = None
            
        if LockContourPipeline:
            try:
                self.contour_pipeline = LockContourPipeline()
            except Exception as e:
                print(f"Pipeline init failed: {e}")
                self.contour_pipeline = None
        else:
            self.contour_pipeline = None

    def process_image(self, image_data: str, scale_factor: Optional[float] = None) -> Dict:
        try:
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                return {
                    "success": False,
                    "error": "Failed to decode image",
                }

            detections = []
            if self.yolo_detector:
                try:
                    detections = self.yolo_detector.detect(image)
                except Exception as e:
                    print(f"YOLO detection failed: {e}")

            measurements = {}
            if self.contour_pipeline:
                try:
                    measurements = self.contour_pipeline.analyze_lock(image)
                except Exception as e:
                    print(f"Pipeline analysis failed: {e}")

            result = {
                "success": True,
                "detections": [
                    {
                        "class": det.class_name,
                        "confidence": det.confidence,
                        "bbox": det.bbox,
                    }
                    for det in detections
                ] if detections else [],
                "measurements": measurements,
            }

            if scale_factor:
                result["scale_factor"] = scale_factor

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def process_image_file(self, image_path: str) -> Dict:
        image = cv2.imread(image_path)
        if image is None:
            return {
                "success": False,
                "error": f"Failed to load image: {image_path}",
            }

        detections = []
        if self.yolo_detector:
            try:
                detections = self.yolo_detector.detect(image)
            except Exception as e:
                print(f"YOLO detection failed: {e}")

        measurements = {}
        if self.contour_pipeline:
            try:
                measurements = self.contour_pipeline.analyze_lock(image)
            except Exception as e:
                print(f"Pipeline analysis failed: {e}")

        return {
            "success": True,
            "detections": [
                {
                    "class": det.class_name,
                    "confidence": det.confidence,
                    "bbox": det.bbox,
                }
                for det in detections
            ] if detections else [],
            "measurements": measurements,
        }


cv_service = CVService()
