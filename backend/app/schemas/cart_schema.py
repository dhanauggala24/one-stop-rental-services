from pydantic import BaseModel
from datetime import date


class CartCreate(BaseModel):

    item_id: int

    start_date: date

    end_date: date