from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # or your actual Base import path

class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_type.id"))
    number = Column(Integer)  # matches the SQL column name
    status = Column(String(255))

    __table_args__ = (
        UniqueConstraint("room_type_id", "number", name="uq_room_type_number"),
    )

    # Relationships
    room_type = relationship("RoomType", back_populates="rooms")
    booking_timeslots = relationship("BookingTimeSlot", back_populates="room")