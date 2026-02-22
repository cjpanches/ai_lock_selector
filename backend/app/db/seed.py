from app.db.models import Lock, Manufacturer, LockTypeEnum
from app.db.database import AsyncSessionLocal


SEED_MANUFACTURERS = [
    {"name": "SecureLock", "country": "Germany", "website": "https://securelock.de"},
    {"name": "DoorGuard", "country": "Italy", "website": "https://doorguard.it"},
    {"name": "SimpleLock", "country": "China", "website": ""},
]


SEED_LOCKS = [
    {
        "vendor_code": "A-001",
        "name": "Замок врезной A",
        "brand": "SecureLock",
        "type": LockTypeEnum.embedded,
        "backset": 55.0,
        "center_distance": 72.0,
        "plate_width": 24.0,
        "plate_height": 235.0,
        "plate_thickness": 3.0,
        "body_width": 85.0,
        "body_height": 165.0,
        "body_depth": 13.0,
        "lock_cylinder_hole": "33x17",
        "square_hole_size": 8.0,
    },
    {
        "vendor_code": "A-002",
        "name": "Замок врезной B",
        "brand": "SecureLock",
        "type": LockTypeEnum.embedded,
        "backset": 72.0,
        "center_distance": 85.0,
        "plate_width": 24.0,
        "plate_height": 235.0,
        "plate_thickness": 3.0,
        "body_width": 85.0,
        "body_height": 165.0,
        "body_depth": 13.0,
        "lock_cylinder_hole": "33x17",
        "square_hole_size": 8.0,
    },
    {
        "vendor_code": "B-001",
        "name": "Замок накладной",
        "brand": "DoorGuard",
        "type": LockTypeEnum.overlay,
        "backset": 0.0,
        "center_distance": 0.0,
        "plate_width": 35.0,
        "plate_height": 180.0,
        "plate_thickness": 5.0,
        "body_width": 90.0,
        "body_height": 130.0,
        "body_depth": 40.0,
    },
    {
        "vendor_code": "C-001",
        "name": "Защёлка",
        "brand": "SimpleLock",
        "type": LockTypeEnum.latch,
        "backset": 0.0,
        "center_distance": 0.0,
        "plate_width": 22.0,
        "plate_height": 150.0,
        "plate_thickness": 2.5,
        "body_width": 65.0,
        "body_height": 100.0,
        "body_depth": 12.0,
        "square_hole_size": 8.0,
    },
    {
        "vendor_code": "A-003",
        "name": "Замок врезной Premium",
        "brand": "SecureLock",
        "type": LockTypeEnum.embedded,
        "backset": 50.0,
        "center_distance": 72.0,
        "plate_width": 26.0,
        "plate_height": 240.0,
        "plate_thickness": 3.5,
        "body_width": 88.0,
        "body_height": 170.0,
        "body_depth": 14.0,
        "lock_cylinder_hole": "33x17",
        "square_hole_size": 9.0,
    },
    {
        "vendor_code": "D-001",
        "name": "Электронный замок",
        "brand": "DoorGuard",
        "type": LockTypeEnum.electronic,
        "backset": 60.0,
        "center_distance": 72.0,
        "plate_width": 28.0,
        "plate_height": 250.0,
        "plate_thickness": 4.0,
        "body_width": 90.0,
        "body_height": 180.0,
        "body_depth": 15.0,
        "lock_cylinder_hole": "33x17",
    },
]


async def seed_database():
    async with AsyncSessionLocal() as session:
        for mfr_data in SEED_MANUFACTURERS:
            mfr = Manufacturer(**mfr_data)
            session.add(mfr)
        
        await session.commit()
        
        from sqlalchemy import select
        result = await session.execute(select(Manufacturer))
        manufacturers = {m.name: m.id for m in result.scalars().all()}
        
        for lock_data in SEED_LOCKS:
            brand = lock_data.pop("brand")
            lock_data["manufacturer_id"] = manufacturers.get(brand)
            lock = Lock(**lock_data)
            session.add(lock)
        
        await session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_database())
