from sqlalchemy.orm import Session
from app.models import Booking, BookingDetail, Invoice, Customer
from app.schemas.booking import BookingDetailCreate, BookingCreate
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession



# Lấy giỏ hàng mới nhất chưa thanh toán
async def get_latest_unpaid_cart(db: AsyncSession, customer_id: int):
    # Use select() for async queries
    result = await db.execute(
        select(Booking).filter(Booking.customer_id == customer_id, Booking.status == "pending").order_by(Booking.created_at.desc())
    )
    # Retrieve the first result
    return result.scalars().first()


# Thêm BookingDetail vào Booking và tạo Hóa Đơn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

async def add_booking_detail(db: AsyncSession, booking_id: int, booking_detail: BookingDetailCreate):
    # Tạo mới một BookingDetail
    new_booking_detail = BookingDetail(
        booking_id=booking_id,
        offer_id=booking_detail.offer_id,
        number_of_rooms=booking_detail.number_of_rooms,
        started_at=booking_detail.started_at,
        finished_at=booking_detail.finished_at,
        status=booking_detail.status,
        cost=booking_detail.number_of_rooms * 100  # giả sử giá mỗi phòng là 100
    )

    # Add BookingDetail to session
    db.add(new_booking_detail)
    await db.flush()  # Use `flush()` to persist the object and generate its ID, but without committing yet

    # Cập nhật Booking (thêm cost của booking_detail vào tổng cost của Booking)
    result = await db.execute(
        select(Booking).filter(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    
    if booking:
        booking.cost += new_booking_detail.cost
        await db.flush()  # Flush changes to the session

    # Commit the changes to save everything
    await db.commit()

    # Refresh and return the new booking detail
    await db.refresh(new_booking_detail)
    return new_booking_detail
