from sqlalchemy import Column, Integer, String, Float, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # or your actual Base import path

class RoomType(Base):
    __tablename__ = "room_type"

    id = Column(Integer, primary_key=True, index=True)
    resort_id = Column(Integer, ForeignKey("resort.id"))
    name = Column(String(255))
    area = Column(Float)
    quantity_standard = Column(String(255))
    quality_standard = Column(String(255))
    bed_amount = Column(Integer)
    people_amount = Column(Integer)
    price = Column(Numeric(12, 2))

    # Relationships
    resort = relationship("Resort", back_populates="room_types")
    rooms = relationship("Room", back_populates="room_type")
    offers = relationship("Offer", back_populates="room_type")
    images = relationship("RoomImage", back_populates="room_type")