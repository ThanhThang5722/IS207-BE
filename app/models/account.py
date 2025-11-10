from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base

# Account Model
class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(String(20), default='ACTIVE')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationship with Customer
    customer = relationship('Customer', back_populates='account', uselist=False)

    # Relationship with Account Token
    tokens = relationship('AccountToken', back_populates='account')

    # Relationship with Role through account_assign_role
    roles = relationship('Role', secondary='account_assign_role', back_populates='accounts')