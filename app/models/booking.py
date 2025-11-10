from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(255))
    cost = Column(Numeric(12, 2))

    # Relationship with Customer
    customer = relationship("Customer", back_populates="bookings")

    # Relationship with BookingDetail
    booking_details = relationship("BookingDetail", back_populates="booking")