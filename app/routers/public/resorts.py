from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db_async import get_db
from app.models.account import Account
from app.models.feedback import Feedback
from app.models.resort import Resort
from app.models.resort_images import ResortImage
from app.models.room_type import RoomType
from app.models.offer import Offer
from app.models.booking_detail import BookingDetail
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.dependencies.auth import get_current_account

router = APIRouter(prefix="/api/v1", tags=["Resorts"])

@router.get("/resorts")
async def get_resort_detail(
    id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    resort_result = await db.execute(select(Resort).where(Resort.id == id))
    resort = resort_result.scalar_one_or_none()

    if not resort:
        raise HTTPException(status_code=404, detail="Resort not found")

    img_result = await db.execute(
        select(ResortImage.url).where(ResortImage.resort_id == id)
    )
    images = [row[0] for row in img_result.all()]

    roomtype_result = await db.execute(
        select(
            RoomType.id,
            RoomType.name,
            RoomType.area,
            RoomType.bed_amount,
            RoomType.people_amount,
            RoomType.price
        ).where(RoomType.resort_id == id)
    )
    room_types = [
        {
            "id": r.id,
            "name": r.name,
            "area": float(r.area),
            "bed_amount": r.bed_amount,
            "people_amount": r.people_amount,
            "price": float(r.price)
        }
        for r in roomtype_result.all()
    ]

    return {
        "id": resort.id,
        "name": resort.name,
        "address": resort.address,
        "rating": resort.rating,
        "images": images,
        "room_types": room_types
    }

@router.get("/resorts/{id}/feedbacks")
async def get_feedbacks(id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Feedback)
        .where(Feedback.resort_id == id)
        .order_by(Feedback.created_at.desc())
    )
    result = await db.execute(stmt)
    feedbacks = result.scalars().all()
    if not feedbacks:
        return []
    
    response = []
    for fb in feedbacks:
        username = None
        if fb.customer and fb.customer.account:
            username = fb.customer.account.username
        
        response.append({
            "id": fb.id,
            "resort_id": fb.resort_id,
            "customer_id": fb.customer_id,
            "rating": fb.rating,
            "comment": fb.comment,
            "created_at": fb.created_at,
            "username": username
        })
    
    return response

@router.post("/resorts/{id}/feedbacks", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def add_feedback(
    id: int,
    feedback: FeedbackCreate,
    current_account: Account = Depends(get_current_account),
    db: AsyncSession = Depends(get_db)
):
    if not current_account.customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản chưa có thông tin khách hàng"
        )
    customer_id = current_account.customer.id

    has_booking = (await db.execute(
        select(BookingDetail.id)
        .join(Offer, BookingDetail.offer_id == Offer.id)
        .join(RoomType, Offer.room_type_id == RoomType.id)
        .where(
            RoomType.resort_id == id,
            BookingDetail.status == "PAID"
        )
        .join(BookingDetail.booking)
        .where(BookingDetail.booking.has(customer_id=customer_id))
        .limit(1)
    )).scalar_one_or_none()

    if not has_booking:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn chỉ có thể đánh giá resort mà bạn đã từng đặt phòng"
        )

    new_feedback = Feedback(
        resort_id=id,
        customer_id=customer_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    return new_feedback
