from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.models import BookingDetail, Invoice
from app.models.offer import Offer
from app.models.room_type import RoomType
from app.models.resort import Resort
from app.database import get_db

router = APIRouter(prefix="/api/v1/customer", tags=["Resorts"])

@router.get("/{id}/histories")
def get_booking_histories(
    id: int,  # customer_id
    db: AsyncSession = Depends(get_db)
):
    # Truy vấn BookingDetails của customer_id có liên kết với Invoice hoặc đã hủy
    result = db.execute(
        select(BookingDetail)
        .join(Invoice, (Invoice.booking_detail_id == BookingDetail.id) & (Invoice.customer_id == id))
        .filter(BookingDetail.status.in_(["PAID", "CANCELLED"]))
        .options(
            selectinload(BookingDetail.offer)
            .selectinload(Offer.room_type)
            .selectinload(RoomType.resort)
        )
        .distinct()
    )

    # Lấy danh sách các booking details đã có hóa đơn
    booking_details = result.scalars().all()

    if not booking_details:
        raise HTTPException(status_code=404, detail="No booking histories found for this customer")

    # Build response với thông tin phòng
    histories = []
    for detail in booking_details:
        offer = detail.offer
        room_type = offer.room_type if offer else None
        resort = room_type.resort if room_type else None
        
        histories.append({
            "id": detail.id,
            "booking_id": detail.booking_id,
            "cost": float(detail.cost) if detail.cost else 0,
            "number_of_rooms": detail.number_of_rooms,
            "started_at": detail.started_at,
            "finished_at": detail.finished_at,
            "status": detail.status,
            "room_type_name": room_type.name if room_type else None,
            "room_type_id": room_type.id if room_type else None,
            "resort_name": resort.name if resort else None,
            "resort_id": resort.id if resort else None,
        })

    return histories
