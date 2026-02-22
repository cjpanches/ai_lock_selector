import cv2
import numpy as np
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class YOLODetection:
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]


class YOLODetector:
    CLASSES = {
        0: "lock_plate",
        1: "cylinder_hole",
        2: "mounting_hole",
        3: "handle_square",
        4: "din_marker",
    }

    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.model_path:
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.model_path)
                print(f"YOLO model loaded from {self.model_path}")
            except ImportError:
                print("Ultralytics not installed, using fallback detection")
                self.model = None
        else:
            print("No model path provided, using fallback detection")

    def detect(self, image: np.ndarray) -> List[YOLODetection]:
        if self.model is not None:
            return self._detect_with_yolo(image)
        else:
            return self._detect_fallback(image)

    def _detect_with_yolo(self, image: np.ndarray) -> List[YOLODetection]:
        results = self.model(image, conf=self.confidence_threshold)
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                class_id = int(box.cls[0])

                detections.append(YOLODetection(
                    class_id=class_id,
                    class_name=self.CLASSES.get(class_id, "unknown"),
                    confidence=conf,
                    bbox=(int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                ))

        return detections

    def _detect_fallback(self, image: np.ndarray) -> List[YOLODetection]:
        detections = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0

            if 0.15 < aspect_ratio < 0.6 and area > 5000:
                detections.append(YOLODetection(
                    class_id=0,
                    class_name="lock_plate",
                    confidence=0.7,
                    bbox=(x, y, w, h)
                ))
            elif area < 500:
                detections.append(YOLODetection(
                    class_id=2,
                    class_name="mounting_hole",
                    confidence=0.6,
                    bbox=(x, y, w, h)
                ))

        return detections

    def get_largest_detection(self, detections: List[YOLODetection], class_name: str = "lock_plate") -> Optional[YOLODetection]:
        filtered = [d for d in detections if d.class_name == class_name]
        if not filtered:
            return None
        return max(filtered, key=lambda d: d.bbox[2] * d.bbox[3])

    def crop_to_detection(self, image: np.ndarray, detection: YOLODetection) -> np.ndarray:
        x, y, w, h = detection.bbox
        margin = 20
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(image.shape[1], x + w + margin)
        y2 = min(image.shape[0], y + h + margin)
        return image[y1:y2, x1:x2]


def detect_lock(image: np.ndarray, model_path: Optional[str] = None) -> Dict:
    detector = YOLODetector(model_path=model_path)
    detections = detector.detect(image)

    result = {
        "success": True,
        "detections": [],
        "lock_plate": None,
        "scale_indicator": None,
    }

    for det in detections:
        result["detections"].append({
            "class": det.class_name,
            "confidence": det.confidence,
            "bbox": det.bbox,
        })

        if det.class_name == "lock_plate":
            result["lock_plate"] = {
                "bbox": det.bbox,
                "confidence": det.confidence,
            }
        elif det.class_name == "din_marker":
            result["scale_indicator"] = {
                "bbox": det.bbox,
                "confidence": det.confidence,
            }

    return result
