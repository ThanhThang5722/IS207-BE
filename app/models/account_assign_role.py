from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base


class AccountAssignRole(Base):
    __tablename__ = 'account_assign_role'

    account_id = Column(Integer, ForeignKey('account.account_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)