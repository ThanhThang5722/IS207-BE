from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    resort_id = Column(Integer, ForeignKey("resort.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    resort = relationship("Resort", back_populates="feedbacks")
    customer = relationship("Customer", back_populates="feedbacks")