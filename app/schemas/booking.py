from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema cho dữ liệu khi tạo BookingDetail
class BookingDetailCreate(BaseModel):
    offer_id: int
    number_of_rooms: int
    started_at: datetime
    finished_at: datetime
    status: str
    customer_id: int
    class Config:
        orm_mode = True


# Schema cho dữ liệu khi tạo Booking
class BookingCreate(BaseModel):
    customer_id: int
    status: str
    cost: Optional[float] = 0.0

    class Config:
        orm_mode = True


# Schema cho dữ liệu trả về của Booking (bao gồm các detail)
class BookingResponse(BaseModel):
    id: int
    #customer_id: int
    created_at: datetime
    status: str
    cost: float
    booking_details: list[BookingDetailCreate]

    class Config:
        orm_mode = True
