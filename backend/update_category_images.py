from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user_model import User
from app.models.item_model import Item

db: Session = SessionLocal()


image_map = {
    "Vehicles": [
    "uploads/vehicles/vehicle1.jpg",
    "uploads/vehicles/vehicle2.png",
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
    "Property Rental": [
        "uploads/property/property1.jpg",
        "uploads/property/property2.jpg",
        "uploads/property/property3.jpg",
        "uploads/property/property4.jpg",
        "uploads/property/property5.jpg",
    ],
    "PG & Hostel": [
        "uploads/pg/pg1.jpg",
        "uploads/pg/pg2.jpg",
        "uploads/pg/pg3.jpg",
        "uploads/pg/pg4.jpg",
        "uploads/pg/pg5.jpg",
    ],
}


try:
    for category, images in image_map.items():
        items = db.query(Item).filter(
            Item.category == category
        ).order_by(Item.id).all()

        for index, item in enumerate(items):
            item.image = images[index % len(images)]

        print(f"{len(items)} {category} images updated")

    db.commit()
    print("All category images updated successfully!")

except Exception as e:
    db.rollback()
    print("Image update failed:", e)

finally:
    db.close()