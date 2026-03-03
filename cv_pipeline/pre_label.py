#!/usr/bin/env python3
"""
Pre-labeling script for YOLO dataset
Uses CV pipeline to auto-generate bounding boxes in YOLO format

Usage:
    python pre_label.py --input images/train --output labels/train
    python pre_label.py --input /path/to/images --output /path/to/labels --visualize
"""

import argparse
import os
import sys
from pathlib import Path
import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

from contour_analyzer import ContourAnalyzer
from edge_detector import EdgeDetector


CLASSES = {
    "lock_plate": 0,
    "cylinder_hole": 1,
    "handle_square": 2,
}

DIN_SLOT_WIDTH_MM = 10.0
MIN_SCALE_FACTOR = 5.0
MAX_SCALE_FACTOR = 50.0
VALID_ASPECT_RATIO_RANGE = (1.5, 4.0)


def yolo_format(x_center, y_center, width, height, img_width, img_height):
    """Convert to YOLO normalized format (0-1)"""
    x_center_norm = x_center / img_width
    y_center_norm = y_center / img_height
    width_norm = width / img_width
    height_norm = height / img_height
    
    x_center_norm = max(0, min(1, x_center_norm))
    y_center_norm = max(0, min(1, y_center_norm))
    width_norm = max(0, min(1, width_norm))
    height_norm = max(0, min(1, height_norm))
    
    return x_center_norm, y_center_norm, width_norm, height_norm


def calculate_scale_from_marker(contours):
    """
    Calculate scale factor from detected Euro cylinder marker.
    Uses the 10mm slot width as reference.
    
    Returns:
        float: pixels_per_mm scale factor, or None if marker not found
    """
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        if area < 100:
            continue
        
        aspect = max(w, h) / min(w, h) if min(w, h) > 0 else 0
        
        if VALID_ASPECT_RATIO_RANGE[0] <= aspect <= VALID_ASPECT_RATIO_RANGE[1]:
            slot_width_px = min(w, h)
            scale = slot_width_px / DIN_SLOT_WIDTH_MM
            
            if MIN_SCALE_FACTOR <= scale <= MAX_SCALE_FACTOR:
                return scale
    
    return None


def process_image(image_path: str, visualize: bool = False):
    """Process single image and return YOLO annotations"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Cannot read image {image_path}")
        return [], None
    
    img_height, img_width = img.shape[:2]
    annotations = []
    
    gray = EdgeDetector.to_grayscale(img)
    blurred = EdgeDetector.gaussian_blur(gray, sigma=1.5, kernel_size=5)
    edges = EdgeDetector.canny_edge_detection(blurred, threshold1=50, threshold2=150)
    
    analyzer = ContourAnalyzer(min_area=100, max_area=50000)
    contours = analyzer.find_contours(edges)
    
    if not contours:
        print(f"Warning: No contours found in {image_path}")
        return [], None
    
    scale_factor = calculate_scale_from_marker(contours)
    if scale_factor is None:
        print(f"Warning: Cannot calculate scale factor for {image_path} - no valid marker detected, skipping")
        return [], None
    
    print(f"  Detected scale factor: {scale_factor:.2f} px/mm")
    
    plate_contour = analyzer.find_plate_contour(contours)
    if plate_contour:
        x, y, w, h = plate_contour.bounding_box
        x_center, y_center, w_norm, h_norm = yolo_format(
            x + w/2, y + h/2, w, h, img_width, img_height
        )
        annotations.append({
            "class_id": CLASSES["lock_plate"],
            "x_center": x_center,
            "y_center": y_center,
            "width": w_norm,
            "height": h_norm,
        })
    
    cylinder_hole = analyzer.find_din_cylinder_hole(contours, scale_factor, tolerance=0.6)
    if cylinder_hole:
        x, y, w, h = cylinder_hole.bounding_box
        x_center, y_center, w_norm, h_norm = yolo_format(
            x + w/2, y + h/2, w, h, img_width, img_height
        )
        annotations.append({
            "class_id": CLASSES["cylinder_hole"],
            "x_center": x_center,
            "y_center": y_center,
            "width": w_norm,
            "height": h_norm,
        })
    
    handle_square = analyzer.find_handle_square(contours, scale_factor)
    if handle_square:
        x, y, w, h = handle_square.bounding_box
        x_center, y_center, w_norm, h_norm = yolo_format(
            x + w/2, y + h/2, w, h, img_width, img_height
        )
        annotations.append({
            "class_id": CLASSES["handle_square"],
            "x_center": x_center,
            "y_center": y_center,
            "width": w_norm,
            "height": h_norm,
        })
    
    if visualize and annotations:
        vis_img = img.copy()
        colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]
        
        for ann in annotations:
            cls_id = ann["class_id"]
            x = int((ann["x_center"] - ann["width"]/2) * img_width)
            y = int((ann["y_center"] - ann["height"]/2) * img_height)
            w = int(ann["width"] * img_width)
            h = int(ann["height"] * img_height)
            
            cv2.rectangle(vis_img, (x, y), (x+w, y+h), colors[cls_id], 2)
            cv2.putText(vis_img, list(CLASSES.keys())[cls_id], (x, y-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[cls_id], 2)
        
        output_path = image_path.replace(".jpg", "_annotated.jpg").replace(".png", "_annotated.png")
        cv2.imwrite(output_path, vis_img)
        print(f"Saved visualization: {output_path}")
    
    return annotations, scale_factor


def save_yolo_annotations(annotations, output_path):
    """Save annotations in YOLO format"""
    with open(output_path, 'w') as f:
        for ann in annotations:
            f.write(f"{ann['class_id']} {ann['x_center']:.6f} {ann['y_center']:.6f} "
                   f"{ann['width']:.6f} {ann['height']:.6f}\n")


def main():
    parser = argparse.ArgumentParser(description="Pre-label images for YOLO training")
    parser.add_argument("--input", "-i", required=True, help="Input directory with images")
    parser.add_argument("--output", "-o", required=True, help="Output directory for labels")
    parser.add_argument("--visualize", "-v", action="store_true", help="Save visualized images")
    parser.add_argument("--extensions", nargs="+", default=[".jpg", ".jpeg", ".png"], 
                       help="Image extensions to process")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    image_files = []
    for ext in args.extensions:
        image_files.extend(input_dir.glob(f"*{ext}"))
        image_files.extend(input_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"No images found in {input_dir}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} images")
    print(f"Processing...")
    
    success_count = 0
    skipped_count = 0
    for img_path in image_files:
        label_path = output_dir / f"{img_path.stem}.txt"
        
        result = process_image(str(img_path), args.visualize)
        
        if result is None:
            skipped_count += 1
            continue
            
        annotations, scale_factor = result
        
        if annotations:
            save_yolo_annotations(annotations, str(label_path))
            success_count += 1
            print(f"  {img_path.name} -> {label_path.name} ({len(annotations)} objects, scale={scale_factor:.2f})")
        else:
            skipped_count += 1
            print(f"  {img_path.name} -> No annotations (scale={scale_factor:.2f})")
    
    print(f"\nDone! Processed {success_count}/{len(image_files)} images")
    print(f"Skipped: {skipped_count} images")
    print(f"Labels saved to: {output_dir}")
    print("\nClasses:")
    for name, cid in CLASSES.items():
        print(f"  {cid}: {name}")


if __name__ == "__main__":
    main()
