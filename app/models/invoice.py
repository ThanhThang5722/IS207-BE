from sqlalchemy import Column, Integer, ForeignKey, Numeric, TIMESTAMP, String
from sqlalchemy.orm import relationship
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    partner_id = Column(Integer, ForeignKey("partner.id"))
    booking_detail_id = Column(Integer, ForeignKey("booking_detail.id"))
    cost = Column(Numeric(12, 2))
    finished_time = Column(TIMESTAMP)
    payment_method = Column(String(255))

    # Relationship with Customer
    customer = relationship("Customer", back_populates="invoices")

    # Relationship with Partner
    partner = relationship("Partner", back_populates="invoices")

    # Relationship with BookingDetail
    booking_detail = relationship("BookingDetail", back_populates="invoices")
    class Config:
        orm_mode = True