import pandas as pd
import random
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.item_model import Item


db: Session = SessionLocal()

ADMIN_OWNER_ID = 4


property_images = [
    "uploads/property/property1.jpg",
    "uploads/property/property2.jpg",
    "uploads/property/property3.jpg",
    "uploads/property/property4.jpg",
    "uploads/property/property5.jpg",
]

pg_images = [
    "uploads/pg/pg1.jpg",
    "uploads/pg/pg2.jpg",
    "uploads/pg/pg3.jpg",
    "uploads/pg/pg4.jpg",
    "uploads/pg/pg5.jpg",
]


def item_exists(title, category):
    return db.query(Item).filter(
        Item.title == title,
        Item.category == category
    ).first() is not None


def import_property_rentals():
    df = pd.read_csv("AB_US_2023.csv", low_memory=False)

    count = 0

    for _, row in df.iterrows():
        try:
            title = str(row["name"])[:100]

            if item_exists(title, "Property Rental"):
                continue

            description = f"{row['room_type']} - {row['neighbourhood']}"[:255]
            location = str(row["city"])[:100]

            try:
                price = float(row["price"])
            except:
                price = 1000

            item = Item(
                title=title,
                description=description,
                location=location,
                price_per_day=price,
                image=random.choice(property_images),
                category="Property Rental",
                approval_status="approved",
                owner_id=ADMIN_OWNER_ID,
            )

            db.add(item)
            count += 1

            if count >= 50:
                break

        except Exception as e:
            print("Skipped Property:", e)

    print(f"{count} Property Rental items imported")


def import_pg_hostels():
    df = pd.read_csv("Travel details dataset.csv", low_memory=False)

    count = 0

    for _, row in df.iterrows():
        try:
            destination = str(row["Destination"])[:100]
            accommodation_type = str(row["Accommodation type"])[:100]

            title = f"{accommodation_type} Stay in {destination}"[:100]

            if item_exists(title, "PG & Hostel"):
                continue

            description = (
                f"{accommodation_type} accommodation suitable for students, "
                f"employees, and travelers."
            )[:255]

            location = destination

            try:
                price = float(row["Accommodation cost"])
            except:
                price = 800

            item = Item(
                title=title,
                description=description,
                location=location,
                price_per_day=price,
                image=random.choice(pg_images),
                category="PG & Hostel",
                approval_status="approved",
                owner_id=ADMIN_OWNER_ID,
            )

            db.add(item)
            count += 1

            if count >= 50:
                break

        except Exception as e:
            print("Skipped PG:", e)

    print(f"{count} PG & Hostel items imported")


import_property_rentals()
import_pg_hostels()

db.commit()
db.close()

print("Dataset import completed successfully!")