#!/usr/bin/env python3
"""
YOLO Training Script for AI Lock Selector
Usage: python train_yolo.py --data lock_dataset.yaml --epochs 100
"""

import argparse
import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    try:
        from ultralytics import YOLO
        return True
    except ImportError:
        print("ERROR: ultralytics not installed")
        print("Install with: pip install ultralytics")
        return False

def prepare_dataset(dataset_yaml: str) -> bool:
    """Check if dataset is ready."""
    dataset_path = Path(dataset_yaml)
    if not dataset_path.exists():
        print(f"ERROR: Dataset config not found: {dataset_yaml}")
        return False
    
    base_path = dataset_path.parent
    
    train_images = base_path / "images" / "train"
    val_images = base_path / "images" / "val"
    
    if not train_images.exists():
        print(f"ERROR: Train images not found: {train_images}")
        return False
    
    if not val_images.exists():
        print(f"ERROR: Val images not found: {val_images}")
        return False
    
    train_count = len(list(train_images.glob("*.jpg"))) + len(list(train_images.glob("*.png")))
    val_count = len(list(val_images.glob("*.jpg"))) + len(list(val_images.glob("*.png")))
    
    print(f"Dataset ready:")
    print(f"  Train images: {train_count}")
    print(f"  Val images: {val_count}")
    
    if train_count < 10:
        print("WARNING: Very few training images. Need 500+ for good accuracy.")
        return False
    
    return True

def train(
    data_yaml: str,
    model_name: str = "yolov8n.pt",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    project: str = "runs/detect",
    name: str = "lock_train",
    pretrained: bool = True,
) -> str:
    """Train YOLO model."""
    from ultralytics import YOLO
    
    print(f"\n{'='*50}")
    print(f"Starting YOLO training")
    print(f"Model: {model_name}")
    print(f"Data: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Image size: {imgsz}")
    print(f"{'='*50}\n")
    
    if pretrained:
        model = YOLO(model_name)
    else:
        model = YOLO(f"{model_name.replace('.pt', '')}.yaml")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        exist_ok=True,
        patience=10,
        save=True,
        plots=True,
        val=True,
        device="cpu",
    )
    
    best_model_path = f"{project}/{name}/weights/best.pt"
    print(f"\nTraining complete!")
    print(f"Best model: {best_model_path}")
    
    return best_model_path

def export_model(model_path: str, format: str = "onnx") -> str:
    """Export trained model to different formats."""
    from ultralytics import YOLO
    
    model = YOLO(model_path)
    export_path = model.export(format=format)
    
    print(f"Model exported to: {export_path}")
    return export_path

def main():
    parser = argparse.ArgumentParser(description="Train YOLO model for lock detection")
    parser.add_argument("--data", type=str, default="dataset/lock_dataset.yaml",
                        help="Path to dataset YAML")
    parser.add_argument("--model", type=str, default="yolov8n-obb.pt",
                        help="YOLO OBB model for oriented bounding boxes")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Number of epochs")
    parser.add_argument("--imgsz", type=int, default=640,
                        help="Image size")
    parser.add_argument("--batch", type=int, default=16,
                        help="Batch size")
    parser.add_argument("--project", type=str, default="runs/detect",
                        help="Project directory")
    parser.add_argument("--name", type=str, default="lock_train",
                        help="Experiment name")
    parser.add_argument("--export", type=str, default=None,
                        help="Export format (onnx, torchscript, tflite)")
    
    args = parser.parse_args()
    
    if not check_requirements():
        sys.exit(1)
    
    if not prepare_dataset(args.data):
        print("\nDataset not ready. Please add images first.")
        print("\nTo annotate images, use:")
        print("  1. LabelImg: https://github.com/tzutalin/labelImg")
        print("  2. Roboflow: https://roboflow.com/")
        print("\nRequired annotations:")
        print("  - lock_plate: Вся планка замка")
        print("  - cylinder_hole: Отверстие цилиндра")
        print("  - mounting_hole: Крепёжные отверстия")
        print("  - handle_square: Квадрат ручки")
        print("  - din_marker: Маркер DIN")
        sys.exit(1)
    
    best_model = train(
        data_yaml=args.data,
        model_name=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
    )
    
    if args.export:
        export_model(best_model, args.export)

if __name__ == "__main__":
    main()
