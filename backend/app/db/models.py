from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class LockTypeEnum(str, enum.Enum):
    embedded = "embedded"
    overlay = "overlay"
    latch = "latch"
    deadbolt = "deadbolt"
    electronic = "electronic"
    cylinder = "cylinder"


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100))
    website = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    locks = relationship("Lock", back_populates="manufacturer")


class Lock(Base):
    __tablename__ = "locks"

    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    brand = Column(String(100), index=True)
    series = Column(String(50))
    color = Column(String(20))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    
    type = Column(Enum(LockTypeEnum), nullable=False, index=True)
    
    backset = Column(Float, nullable=False)
    center_distance = Column(Float, nullable=False)
    
    plate_width = Column(Float)
    plate_height = Column(Float)
    plate_thickness = Column(Float)
    
    body_width = Column(Float)
    body_height = Column(Float)
    body_depth = Column(Float)
    
    lock_cylinder_hole = Column(String(20))
    square_hole_size = Column(Float)
    
    package_type = Column(String(20))
    package_qty = Column(Integer)
    minibox_qty = Column(Integer)
    
    purpose = Column(String(50))
    for_entry_doors = Column(String(10))
    for_interior_doors = Column(String(10))
    mounting_type = Column(String(50))
    
    bolt_type = Column(String(50))
    bolt_count = Column(Integer)
    bolt_throw = Column(Float)
    bolt_diameter = Column(Float)
    
    mechanism_type = Column(String(50))
    key_type = Column(String(50))
    key_count = Column(Integer)
    cylinder_included = Column(String(20))
    cylinder_size = Column(String(20))
    cylinder_material = Column(String(50))
    
    image_url = Column(String(500))
    drawing_url = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    manufacturer = relationship("Manufacturer", back_populates="locks")
    compatibility = relationship("LockCompatibility", back_populates="lock")


class LockCompatibility(Base):
    __tablename__ = "lock_compatibility"

    id = Column(Integer, primary_key=True, index=True)
    lock_id = Column(Integer, ForeignKey("locks.id"), nullable=False)
    compatible_with_vendor_code = Column(String(50), nullable=False)
    compatibility_type = Column(String(50))
    notes = Column(Text)

    lock = relationship("Lock", back_populates="compatibility")


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    lock_id = Column(Integer, ForeignKey("locks.id"))
    
    backset_measured = Column(Float)
    center_distance_measured = Column(Float)
    plate_width_measured = Column(Float)
    plate_height_measured = Column(Float)
    
    confidence = Column(Float)
    image_path = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
