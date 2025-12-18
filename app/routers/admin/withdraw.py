from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, date
from app.models import Partner
from app.models.withdraw import Withdraw
from app.database import get_db

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Withdraw Management"])

@router.get("/withdraws")
def get_withdraw_requests(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    status: str | None = Query(None, description="Lọc theo trạng thái: PENDING/APPROVED/REJECTED"),
    partner_id: int | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None)
):
    print('here')
    # Base query
    query = select(Withdraw, Partner.name).join(Partner, Withdraw.partner_id == Partner.id)

    filters = []
    if status:
        filters.append(Withdraw.status == status)
    if partner_id:
        filters.append(Withdraw.partner_id == partner_id)
    if start_date:
        filters.append(Withdraw.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        filters.append(Withdraw.created_at <= datetime.combine(end_date, datetime.max.time()))

    if filters:
        query = query.where(and_(*filters))

    # Count tổng số bản ghi
    count_query = select(func.count()).select_from(Withdraw)
    if filters:
        count_query = count_query.where(and_(*filters))
    total_result = db.execute(count_query)
    total = total_result.scalar()

    # Lấy dữ liệu trang hiện tại
    result = db.execute(
        query.order_by(Withdraw.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    withdraws = result.all()

    data = [
        {
            "id": w.Withdraw.id,
            "partner_id": w.Withdraw.partner_id,
            "partner_name": w.name,
            "transaction_amount": float(w.Withdraw.transaction_amount),
            "status": w.Withdraw.status,
            "created_at": w.Withdraw.created_at,
            "finished_at": w.Withdraw.finished_at
        }
        for w in withdraws
    ]

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": data
    }


@router.post("/withdraws")
def approve_withdraw_request(
    id: int = Query(..., description="ID của yêu cầu rút tiền"),
    db: AsyncSession = Depends(get_db)
):
    # 1️⃣ Tìm yêu cầu rút tiền
    result = db.execute(select(Withdraw).where(Withdraw.id == id))
    withdraw = result.scalar_one_or_none()

    if not withdraw:
        raise HTTPException(status_code=404, detail="Withdraw request not found")

    # 2️⃣ Kiểm tra trạng thái
    if withdraw.status != "pending":
        raise HTTPException(status_code=400, detail=f"Cannot approve withdraw in status '{withdraw.status}'")

    # 3️⃣ Cập nhật trạng thái
    withdraw.status = "approved"
    withdraw.finished_at = datetime.utcnow()

    # 4️⃣ (Optional) Ghi log hoặc tạo transaction entry
    # Có thể thêm bảng transaction_history nếu muốn lưu lại hoạt động này

    db.add(withdraw)
    db.commit()
    db.refresh(withdraw)

    return {
        "message": "Withdraw request approved successfully",
        "withdraw_id": withdraw.id,
        "partner_id": withdraw.partner_id,
        "amount": float(withdraw.transaction_amount),
        "status": withdraw.status,
        "finished_at": withdraw.finished_at
    }