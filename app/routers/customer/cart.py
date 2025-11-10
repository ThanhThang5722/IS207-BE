from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from app.models.booking_detail import BookingDetail
from app.models.invoice import Invoice
from app.models.number_of_room import BookingDetailUpdate
from app.schemas.booking import BookingDetailCreate
from app.database import get_db
from app.schemas.payment import PaymentRequest
from app.services import crud_booking as crud

router = APIRouter(prefix="/api/v1", tags=["Resorts"])

@router.post("/booking", response_model=BookingDetailCreate, status_code=status.HTTP_201_CREATED)
async def add_booking(booking_detail: BookingDetailCreate, db: AsyncSession = Depends(get_db)):
    # Lấy giỏ hàng chưa thanh toán của customer
    cart = await crud.get_latest_unpaid_cart(db=db, customer_id=booking_detail.customer_id)
    
    if not cart:
        raise HTTPException(status_code=404, detail="Không có giỏ hàng chưa thanh toán.")

    # Thêm BookingDetail vào giỏ và tạo Hóa Đơn
    await crud.add_booking_detail(db=db, booking_id=cart.id, booking_detail=booking_detail)

    return booking_detail

@router.put("/booking-detail/{booking_detail_id}")
async def update_booking_detail(
    booking_detail_id: int, 
    booking_detail_update: BookingDetailUpdate, 
    db: AsyncSession = Depends(get_db)
):
    # Tìm booking_detail theo ID
    result = await db.execute(select(BookingDetail).filter(BookingDetail.id == booking_detail_id))
    booking_detail = result.scalar_one_or_none()
    
    # Kiểm tra xem booking_detail có tồn tại không
    if not booking_detail:
        raise HTTPException(status_code=404, detail="Booking Detail not found")
    
    # Cập nhật số lượng phòng
    booking_detail.number_of_rooms = booking_detail_update.number_of_rooms
    
    # Tính lại tổng chi phí (nếu cần), ví dụ: nếu giá phòng thay đổi
    booking_detail.cost = booking_detail.number_of_rooms * 100  # Giả sử giá phòng là 100, thay đổi nếu cần
    
    # Commit và refresh lại booking_detail
    db.add(booking_detail)
    await db.commit()
    await db.refresh(booking_detail)

    return {"message": "Booking Detail updated successfully", "booking_detail": booking_detail}

@router.post("/payment")
async def process_payment(
    payment_request: PaymentRequest, 
    db: AsyncSession = Depends(get_db)
):
    # Tìm BookingDetail theo booking_detail_id trong một ngữ cảnh bất đồng bộ đúng
    result = await db.execute(select(BookingDetail).filter(BookingDetail.id == payment_request.booking_detail_id).options(selectinload(BookingDetail.booking)))
    booking_detail = result.scalar_one_or_none()

    if not booking_detail:
        raise HTTPException(status_code=404, detail="Booking Detail not found")

    # Kiểm tra trạng thái thanh toán
    if payment_request.payment_status != "success":
        raise HTTPException(status_code=400, detail="Payment not successful")

    # Cập nhật trạng thái của booking_detail thành "PAID"
    booking_detail.status = "PAID"
    db.add(booking_detail)
    await db.commit()  # Chắc chắn là await đúng
    await db.refresh(booking_detail)  # Đảm bảo refresh sau khi commit

    # Tạo hóa đơn
    invoice = Invoice(
        customer_id=booking_detail.booking.customer_id,  # Giả sử bạn có mối quan hệ booking với customer
        partner_id=1,  # Partner ID có thể là một giá trị cố định hoặc từ hệ thống
        booking_detail_id=booking_detail.id,
        cost=payment_request.paid_amount,
        payment_method=payment_request.payment_method,
    )
    db.add(invoice)
    await db.commit()  # Chắc chắn là await đúng
    await db.refresh(invoice)  # Đảm bảo refresh sau khi commit

    # Trả về hóa đơn đã tạo
    return invoice
