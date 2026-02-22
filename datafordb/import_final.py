#!/usr/bin/env python3
"""
Import locks from CSV to database
"""

import csv
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.db.database import AsyncSessionLocal, init_db
from app.db.models import Lock, Manufacturer, LockTypeEnum


def detect_lock_type(name: str, series: str) -> LockTypeEnum:
    """Detect lock type from name."""
    name_lower = name.lower()
    
    if 'противопожарный' in name_lower or 'огнестойкий' in name_lower:
        return LockTypeEnum.embedded
    
    if 'сувальд' in name_lower:
        return LockTypeEnum.deadbolt
    
    if 'защёлка' in name_lower or ' latch' in name_lower:
        return LockTypeEnum.latch
    
    if 'накладной' in name_lower:
        return LockTypeEnum.overlay
    
    if 'электрон' in name_lower or 'электром' in name_lower:
        return LockTypeEnum.electronic
    
    return LockTypeEnum.embedded


async def import_locks(csv_path: str):
    """Import locks from CSV file."""
    await init_db()
    
    async with AsyncSessionLocal() as session:
        mfr = Manufacturer(name="Apecs", country="Китай", website="https://apecs.ru")
        session.add(mfr)
        await session.commit()
        await session.refresh(mfr)
        
        locks_count = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if not row.get('backset') or not row.get('center_distance'):
                    continue
                
                backset = float(row.get('backset', 0) or 0)
                center_distance = float(row.get('center_distance', 0) or 0)
                
                if backset == 0 or center_distance == 0:
                    continue
                
                lock = Lock(
                    vendor_code=row.get('vendor_code', '')[:50],
                    name=row.get('name', ''),
                    description=row.get('description', ''),
                    brand=row.get('brand', 'Apecs'),
                    series=row.get('series', ''),
                    color=row.get('color', ''),
                    manufacturer_id=mfr.id,
                    type=detect_lock_type(row.get('name', ''), row.get('series', '')),
                    
                    backset=backset,
                    center_distance=center_distance,
                    
                    plate_width=float(row.get('plate_width', 0) or 0) or None,
                    plate_height=float(row.get('plate_height', 0) or 0) or None,
                    plate_thickness=float(row.get('plate_thickness', 0) or 0) or None,
                    
                    body_width=float(row.get('body_width', 0) or 0) or None,
                    body_height=float(row.get('body_height', 0) or 0) or None,
                    body_depth=float(row.get('body_depth', 0) or 0) or None,
                    
                    lock_cylinder_hole=row.get('lock_cylinder_hole', '') or None,
                    square_hole_size=float(row.get('square_hole_size', 0) or 0) or None,
                    
                    package_type=row.get('package_type', '') or None,
                    package_qty=int(row.get('package_qty', 0) or 0) or None,
                    minibox_qty=int(row.get('minibox_qty', 0) or 0) or None,
                    
                    purpose=row.get('purpose', '') or None,
                    for_entry_doors=row.get('for_entry_doors', '') or None,
                    for_interior_doors=row.get('for_interior_doors', '') or None,
                    mounting_type=row.get('mounting_type', '') or None,
                    
                    bolt_type=row.get('bolt_type', '') or None,
                    bolt_count=int(row.get('bolt_count', 0) or 0) or None,
                    bolt_throw=float(row.get('bolt_throw', 0) or 0) or None,
                    bolt_diameter=float(row.get('bolt_diameter', 0) or 0) or None,
                    
                    mechanism_type=row.get('mechanism_type', '') or None,
                    key_type=row.get('key_type', '') or None,
                    key_count=int(row.get('key_count', 0) or 0) or None,
                    cylinder_included=row.get('cylinder_included', '') or None,
                    cylinder_size=row.get('cylinder_size', '') or None,
                    cylinder_material=row.get('cylinder_material', '') or None,
                )
                
                session.add(lock)
                locks_count += 1
        
        await session.commit()
        
        print(f"Imported {locks_count} locks to database")


if __name__ == "__main__":
    csv_path = "/home/bot/porojects/ai_lock_project/datafordb/locks_final.csv"
    asyncio.run(import_locks(csv_path))
