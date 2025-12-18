from pydantic import BaseModel
from typing import Optional


class CreatePaymentRequest(BaseModel):
    booking_id: int
    redirect_url: Optional[str] = ""


class CreatePaymentResponse(BaseModel):
    return_code: int
    return_message: str
    order_url: Optional[str] = None
    app_trans_id: Optional[str] = None
    zp_trans_token: Optional[str] = None


class ZaloPayCallback(BaseModel):
    data: str
    mac: str
    type: int


class QueryPaymentRequest(BaseModel):
    app_trans_id: str


class QueryPaymentResponse(BaseModel):
    return_code: int
    return_message: str
    is_processing: Optional[bool] = None
    amount: Optional[int] = None
    zp_trans_id: Optional[int] = None
