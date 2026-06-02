from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user_model import User
from app.models.item_model import Item


db: Session = SessionLocal()


image_map = {
    "Vehicles": [
        "uploads/vehicles/vehicle1.jpg",
        "uploads/vehicles/vehicle2.jpg",
        "uploads/vehicles/vehicle3.jpg",
        "uploads/vehicles/vehicle4.jpg",
        "uploads/vehicles/vehicle5.jpg",
    ],
    "Photography": [
        "uploads/photography/camera1.jpg",
        "uploads/photography/camera2.jpg",
        "uploads/photography/camera3.jpg",
        "uploads/photography/camera4.jpg",
        "uploads/photography/camera5.jpg",
    ],
    "Equipment": [
        "uploads/equipment/equipment1.jpg",
        "uploads/equipment/equipment2.jpg",
        "uploads/equipment/equipment3.jpg",
        "uploads/equipment/equipment4.jpg",
        "uploads/equipment/equipment5.jpg",
    ],
    "Camping": [
        "uploads/camping/camping1.jpg",
        "uploads/camping/camping2.jpg",
        "uploads/camping/camping3.jpg",
        "uploads/camping/camping4.jpg",
        "uploads/camping/camping5.jpg",
    ],
}


for category, images in image_map.items():
    items = db.query(Item).filter(Item.category == category).all()

    for index, item in enumerate(items):
        item.image = images[index % len(images)]

    print(f"{len(items)} {category} images updated")


db.commit()
db.close()

print("All category images updated successfully!")