from pydantic import BaseModel


class ItemCreate(BaseModel):

    title: str

    description: str

    price_per_day: float

    location: str

    category: str = "Property Rental"