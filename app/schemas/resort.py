from pydantic import BaseModel
from typing import List, Optional

from pydantic import BaseModel

class ResortBase(BaseModel):
    name: str
    address: str | None = None
    rating: float | None = None
    price: float | None = None

class ResortCreate(ResortBase):
    pass

class ResortOut(ResortBase):
    id: int

    class Config:
        orm_mode = True  # Cho phép trả về trực tiếp object từ SQLAlchemy

class ResortSummary(BaseModel):
    id: int
    name: str
    address: Optional[str]
    rating: Optional[int]
    images: List[str] = []
    services: List[str] = []

    class Config:
        orm_mode = True
