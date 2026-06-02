from app.database.database import engine, Base

from app.models.user_model import User
from app.models.item_model import Item
from app.models.booking_model import Booking


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully ✅")