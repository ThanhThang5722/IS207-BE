from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))

    # Relationship with Account through account_assign_role
    accounts = relationship('Account', secondary='account_assign_role', back_populates='roles')