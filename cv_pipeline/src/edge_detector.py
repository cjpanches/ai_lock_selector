import cv2
import numpy as np
from typing import List as TypingList, Tuple


class EdgeDetector:
    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    @staticmethod
    def gaussian_blur(image: np.ndarray, sigma: float = 1.5, kernel_size: int = 5) -> np.ndarray:
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    
    @staticmethod
    def canny_edge_detection(image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
        return cv2.Canny(image, threshold1, threshold2)
    
    @staticmethod
    def adaptive_threshold(image: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:
        gray = EdgeDetector.to_grayscale(image)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, block_size, c)
    
    @staticmethod
    def dilate(image: np.ndarray, iterations: int = 1, kernel_size: int = 3) -> np.ndarray:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(image, kernel, iterations=iterations)
    
    @staticmethod
    def erode(image: np.ndarray, iterations: int = 1, kernel_size: int = 3) -> np.ndarray:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(image, kernel, iterations=iterations)
    
    @staticmethod
    def morphology_ex(image: np.ndarray, operation: str, kernel_size: int = 5) -> np.ndarray:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        operations = {
            'open': cv2.MORPH_OPEN,
            'close': cv2.MORPH_CLOSE,
            'gradient': cv2.MORPH_GRADIENT,
            'tophat': cv2.MORPH_TOPHAT,
            'blackhat': cv2.MORPH_BLACKHAT,
        }
        
        op = operations.get(operation, cv2.MORPH_CLOSE)
        return cv2.morphologyEx(image, op, kernel)
    
    @staticmethod
    def perspective_transform(image: np.ndarray, points: np.ndarray) -> np.ndarray:
        if len(points) != 4:
            raise ValueError("Exactly 4 points required for perspective transform")
        
        pts1 = np.float32(points)
        width = int(max(
            np.linalg.norm(pts1[0] - pts1[1]),
            np.linalg.norm(pts1[2] - pts1[3])
        ))
        height = int(max(
            np.linalg.norm(pts1[0] - pts1[3]),
            np.linalg.norm(pts1[1] - pts1[2])
        ))
        
        pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(image, matrix, (width, height))

    @staticmethod
    def find_contours_external(edges: np.ndarray) -> TypingList[np.ndarray]:
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def find_contours_hierarchical(edges: np.ndarray) -> Tuple[TypingList[np.ndarray], any]:
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy
