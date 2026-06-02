from sqlalchemy import Column, Integer, ForeignKey, Date
from app.database.database import Base


class Cart(Base):

    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    start_date = Column(Date)

    end_date = Column(Date)

    total_price = Column(Integer)