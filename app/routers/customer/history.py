from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import BookingDetail, Invoice
from app.database import get_db

router = APIRouter(prefix="/api/v1/customer", tags=["Resorts"])

@router.get("/{id}/histories")
async def get_booking_histories(
    id: int,  # customer_id
    db: AsyncSession = Depends(get_db)
):
    #print('here')
    # Truy vấn BookingDetails của customer_id có liên kết với Invoice
    result = await db.execute(
        select(BookingDetail)
        .join(Invoice, (Invoice.booking_detail_id == BookingDetail.id) & (Invoice.customer_id == id))
    )

    # Lấy danh sách các booking details đã có hóa đơn
    booking_details = result.scalars().all()

    if not booking_details:
        raise HTTPException(status_code=404, detail="No booking histories found for this customer")

    # Trả về danh sách booking detail
    return booking_details
