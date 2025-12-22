from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db_async import get_db
from app.models.room_type import RoomType
from app.models.offer import Offer
from app.models.room_images import RoomImage

router = APIRouter(prefix="/api/v1", tags=["RoomType"])

class RoomTypeRequest(BaseModel):
    room_type_ids: list[int]


@router.post("/roomtypes/details")
async def get_roomtype_details(
    payload: RoomTypeRequest,
    db: AsyncSession = Depends(get_db)
):
    if not payload.room_type_ids:
        raise HTTPException(status_code=400, detail="room_type_ids cannot be empty")

    stmt = select(
        RoomType.id,
        RoomType.name,
        RoomType.area,
        RoomType.people_amount,
        RoomType.price
    ).where(RoomType.id.in_(payload.room_type_ids))

    result = await db.execute(stmt)
    room_types = result.all()

    if not room_types:
        raise HTTPException(status_code=404, detail="No room types found")

    output = []

    for rt in room_types:
        offers_result = await db.execute(
            select(Offer.id, Offer.cost)
            .where(Offer.room_type_id == rt.id)
        )
        offers = [{"id": o.id, "cost": float(o.cost)} for o in offers_result.all()]

        img_result = await db.execute(
            select(RoomImage.url)
            .where(RoomImage.room_type_id == rt.id, RoomImage.is_deleted == False)
        )
        images = [row[0] for row in img_result.all()]

        output.append({
            "id": rt.id,
            "name": rt.name,
            "area": float(rt.area),
            "people_amount": rt.people_amount,
            "price": float(rt.price),
            "offers": offers,
            "images": images
        })

    return output
