from pydantic import BaseModel
from datetime import datetime

class PaymentRequest(BaseModel):
    booking_detail_id: int
    payment_status: str  # Ví dụ: "success" hoặc "failed"
    paid_amount: float
    payment_method: str  # Ví dụ: "CASH", "CARD"
    payment_time: datetime  # Thời gian thanh toán

    class Config:
        orm_mode = True