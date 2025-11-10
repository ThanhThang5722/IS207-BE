from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database import Base

class AccountToken(Base):
    __tablename__ = 'account_token'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    token_value = Column(String(500), nullable=False)
    expires_at = Column(TIMESTAMP)
    issued_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_revoked = Column(Boolean, default=False)

    # Relationship with Account
    account = relationship('Account', back_populates='tokens')