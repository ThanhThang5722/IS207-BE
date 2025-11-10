# app/models/room_images.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(Integer, primary_key=True)
    room_type_id = Column(Integer, ForeignKey("room_type.id"))
    url = Column(String(255))
    is_deleted = Column(Boolean, default=False)

    room_type = relationship("RoomType", back_populates="images")
