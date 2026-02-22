from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.cv_service import cv_service

router = APIRouter()


class CVProcessRequest(BaseModel):
    image: str
    scale_factor: Optional[float] = None
    marker_x: Optional[float] = None
    marker_y: Optional[float] = None


@router.post("/process")
async def process_image(request: CVProcessRequest):
    """Обработка изображения с использованием YOLO + CV"""
    result = cv_service.process_image(
        image_data=request.image,
        scale_factor=request.scale_factor,
    )
    
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Processing failed"))
    
    return result


@router.post("/detect")
async def detect_lock(request: CVProcessRequest):
    """Детекция замка на изображении"""
    result = cv_service.process_image(
        image_data=request.image,
    )
    
    return result


@router.get("/pipeline/{image_name}")
async def process_image_file(image_name: str):
    """Обработка изображения по имени файла"""
    import os
    from pathlib import Path
    
    upload_dir = Path("uploads")
    image_path = upload_dir / image_name
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    result = cv_service.process_image_file(str(image_path))
    
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Processing failed"))
    
    return result
