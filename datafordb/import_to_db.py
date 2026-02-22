#!/usr/bin/env python3
"""
Import locks from CSV to database
"""

import csv
import re
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.db.database import AsyncSessionLocal, init_db
from app.db.models import Lock, Manufacturer, LockTypeEnum


def parse_mm(value: str) -> float:
    """Parse mm value from string."""
    if not value:
        return 0.0
    match = re.search(r'([\d.]+)', value.replace(',', '.'))
    if match:
        return float(match.group(1))
    return 0.0


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
                
                backset = parse_mm(row.get('backset', ''))
                center_distance = parse_mm(row.get('center_distance', ''))
                
                if backset == 0 or center_distance == 0:
                    continue
                
                lock = Lock(
                    vendor_code=row.get('vendor_code', '')[:50],
                    name=row.get('name', ''),
                    brand=row.get('brand', 'Apecs'),
                    manufacturer_id=mfr.id,
                    type=detect_lock_type(row.get('name', ''), row.get('series', '')),
                    backset=backset,
                    center_distance=center_distance,
                    plate_width=24.0,
                    plate_height=235.0,
                    plate_thickness=3.0,
                    body_width=85.0,
                    body_height=165.0,
                    body_depth=13.0,
                )
                
                if row.get('cylinder_size'):
                    cylinder_match = re.search(r'(\d+)/(\d+)', row['cylinder_size'])
                    if cylinder_match:
                        lock.cylinder_hole_diameter = float(cylinder_match.group(1)) * 2
                
                if row.get('bolt_count'):
                    try:
                        lock.square_hole_size = 8.0
                    except ValueError:
                        pass
                
                session.add(lock)
                locks_count += 1
        
        await session.commit()
        
        print(f"Imported {locks_count} locks to database")


if __name__ == "__main__":
    csv_path = "/home/bot/porojects/ai_lock_project/datafordb/locks_parsed.csv"
    asyncio.run(import_locks(csv_path))
