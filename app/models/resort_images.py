from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base  # or your actual Base import path

class ResortImage(Base):
    __tablename__ = "resort_images"

    id = Column(Integer, primary_key=True, index=True)
    resort_id = Column(Integer, ForeignKey("resort.id"))
    url = Column(String(255))

    resort = relationship("Resort", back_populates="images")