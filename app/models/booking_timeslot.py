from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base  # adjust import if needed

class BookingTimeSlot(Base):
    __tablename__ = "booking_timeslot"

    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)
    started_time = Column(DateTime, primary_key=True)  # matches SQL timestamp
    finished_time = Column(DateTime)  # matches SQL timestamp
    invoice_id = Column(Integer)  # Assuming you want to add this field

    __table_args__ = (
        UniqueConstraint("room_id", "started_time", name="uq_room_started_time"),  # Unique constraint adjusted
    )
    # Relationships
    room = relationship("Room", back_populates="booking_timeslots")