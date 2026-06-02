from sqlalchemy import Column, Integer, ForeignKey, String, Date
from app.database.database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    item_id = Column(Integer, ForeignKey("items.id"))

    renter_id = Column(Integer, ForeignKey("users.id"))

    start_date = Column(Date)

    end_date = Column(Date)

    status = Column(String, default="pending")