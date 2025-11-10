from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base

class Partner(Base):
    __tablename__ = 'partner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    name = Column(String(100))
    phone_number = Column(String(10))
    address = Column(String(255))
    banking_number = Column(String(20))
    bank = Column(String(255))
    balance = Column(Numeric(12, 2), default=0)

    # Relationship with Account
    resorts = relationship("Resort", back_populates="partner")
    account = relationship('Account')
    invoices = relationship("Invoice", back_populates="partner")