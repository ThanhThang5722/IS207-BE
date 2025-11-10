from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, foreign
from app.database import Base
from app.models.partner import Partner

class Resort(Base):
    __tablename__ = "resort"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partner.id"), nullable=False)
    name = Column(String)
    address = Column(String)
    ward_id = Column(Integer)
    img_360_url = Column(String)
    rating = Column(Integer, default=0)

    images = relationship("ResortImage", back_populates="resort")
    services = relationship("Service", back_populates="resort")
    room_types = relationship("RoomType", back_populates="resort")
    feedbacks = relationship("Feedback", back_populates="resort")
    partner = relationship("Partner", back_populates="resorts")