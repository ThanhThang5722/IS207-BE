from pydantic import BaseModel

class BookingDetailUpdate(BaseModel):
    number_of_rooms: int
    