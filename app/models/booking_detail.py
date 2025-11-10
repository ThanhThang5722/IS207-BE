from sqlalchemy import Column, Integer, ForeignKey, Numeric, TIMESTAMP, String
from sqlalchemy.orm import relationship
from app.database import Base

class BookingDetail(Base):
    __tablename__ = "booking_detail"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("booking.id"))
    offer_id = Column(Integer, ForeignKey("offer.id"))  # Assuming an `Offer` model exists
    number_of_rooms = Column(Integer)
    cost = Column(Numeric(12, 2))
    started_at = Column(TIMESTAMP)
    finished_at = Column(TIMESTAMP)
    status = Column(String(255))
    # Relationship with Booking
    booking = relationship("Booking", back_populates="booking_details")

    # Relationship with Offer (assuming Offer model exists)
    offer = relationship("Offer", back_populates="booking_details")
    # Relationship with Invoice
    invoices = relationship("Invoice", back_populates="booking_detail")
    class Config:
        orm_mode = True