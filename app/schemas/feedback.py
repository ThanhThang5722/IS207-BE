from pydantic import BaseModel, Field
from datetime import datetime

class FeedbackCreate(BaseModel):
    customer_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None

class FeedbackResponse(BaseModel):
    id: int
    resort_id: int
    customer_id: int | None = None
    rating: int
    comment: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True