from pydantic import BaseModel
from datetime import date


# CREATE BOOKING

class BookingCreate(BaseModel):

    item_id: int

    start_date: date

    end_date: date


# BOOKING RESPONSE

class BookingResponse(BaseModel):

    booking_id: int

    item_title: str

    location: str

    start_date: date

    end_date: date

    status: str