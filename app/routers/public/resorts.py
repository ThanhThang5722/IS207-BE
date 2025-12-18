from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.feedback import Feedback
from app.models.resort import Resort
from app.models.resort_images import ResortImage
from app.models.room_type import RoomType
from app.models.offer import Offer
from app.models.booking_detail import BookingDetail
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.routers.public.auth import get_current_account

router = APIRouter(prefix="/api/v1", tags=["Resorts"])

@router.get("/resorts")
def get_resort_detail(
    id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    # 1️⃣ Lấy thông tin resort
    resort_result = db.execute(select(Resort).where(Resort.id == id))
    resort = resort_result.scalar_one_or_none()

    if not resort:
        raise HTTPException(status_code=404, detail="Resort not found")

    # 2️⃣ Lấy ảnh
    img_result = db.execute(
        select(ResortImage.url).where(ResortImage.resort_id == id)
    )
    images = [row[0] for row in img_result.all()]

    # 3️⃣ Lấy danh sách loại phòng
    roomtype_result = db.execute(
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

    # 4️⃣ Kết hợp thành output
    return {
        "id": resort.id,
        "name": resort.name,
        "address": resort.address,
        "rating": resort.rating,
        "images": images,
        "room_types": room_types
    }

@router.get("/resorts/{id}/feedbacks", response_model=list[FeedbackResponse])
def get_feedbacks(id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Feedback)
        .where(Feedback.resort_id == id)
        .order_by(Feedback.created_at.desc())
    )
    result = db.execute(stmt)
    feedbacks = result.scalars().all()
    if not feedbacks:
        # Không ném lỗi, trả rỗng vẫn OK — tuỳ bạn
        return []
    return feedbacks

@router.post("/resorts/{id}/feedbacks", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def add_feedback(
    id: int,
    feedback: FeedbackCreate,
    current_account: Account = Depends(get_current_account),
    db: AsyncSession = Depends(get_db)
):
    # Lấy customer_id từ token
    if not current_account.customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản chưa có thông tin khách hàng"
        )
    customer_id = current_account.customer.id

    # Kiểm tra customer đã từng đặt phòng ở resort này chưa
    has_booking = db.execute(
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
    ).scalar_one_or_none()

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
    db.commit()
    db.refresh(new_feedback)
    return new_feedback