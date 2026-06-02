from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.database import Base


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    price_per_day = Column(Float)

    location = Column(String)

    image = Column(String, nullable=True)

    category = Column(String, default="Property Rental")

    approval_status = Column(String, default="pending")

    owner_id = Column(Integer, ForeignKey("users.id"))