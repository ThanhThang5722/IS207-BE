from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base

class Withdraw(Base):
    __tablename__ = 'withdraw'

    id = Column(Integer, primary_key=True, autoincrement=True)
    partner_id = Column(Integer, ForeignKey('partner.id'), nullable=False)
    transaction_amount = Column(Numeric(12, 2))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    finished_at = Column(TIMESTAMP)
    status = Column(String(255))

    # Relationship with Partner
    partner = relationship('Partner')


