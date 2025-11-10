from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from app.database import Base

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    fullname = Column(String(100))
    email = Column(String(150), unique=True)
    phone_number = Column(String(10))
    id_number = Column(String(15))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationship with Account
    account = relationship('Account', back_populates='customer')
    feedbacks = relationship("Feedback", back_populates="customer")
    bookings = relationship("Booking", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")