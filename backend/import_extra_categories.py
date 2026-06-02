from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.item_model import Item
from app.models.user_model import User
from app.services.hash_service import hash_password

db: Session = SessionLocal()


def get_or_create_admin():
    admin = db.query(User).filter(User.email == "admin@onestoprentals.com").first()

    if admin:
        return admin.id

    admin = User(
        name="Admin",
        email="admin@onestoprentals.com",
        phone_number="9999999999",
        password=hash_password("admin123"),
        role="admin",
        provider_status="not_requested"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin.id


ADMIN_OWNER_ID = get_or_create_admin()

locations = [
    "Guntur",
    "Vijayawada",
    "Hyderabad",
    "Visakhapatnam",
    "Tirupati",
    "Warangal",
    "Chennai",
    "Bangalore",
    "Pune",
    "Mumbai",
]

vehicles = [
    ("Honda Activa", "uploads/vehicles/vehicle1.jpg"),
    ("TVS Jupiter", "uploads/vehicles/vehicle2.png"),
    ("Royal Enfield Classic 350", "uploads/vehicles/vehicle3.jpg"),
    ("Bajaj Pulsar", "uploads/vehicles/vehicle4.jpg"),
    ("Yamaha FZ", "uploads/vehicles/vehicle5.jpg"),
    ("Maruti Swift", "uploads/vehicles/vehicle1.jpg"),
    ("Hyundai i20", "uploads/vehicles/vehicle2.png"),
    ("Tata Nexon", "uploads/vehicles/vehicle3.jpg"),
    ("Mahindra Thar", "uploads/vehicles/vehicle4.jpg"),
    ("Toyota Innova", "uploads/vehicles/vehicle5.jpg"),
]

photography = [
    ("Canon EOS 1500D", "uploads/photography/photo1.jpg"),
    ("Nikon D5600", "uploads/photography/photo2.jpg"),
    ("Sony Alpha A6400", "uploads/photography/photo3.jpg"),
    ("Canon 50mm Lens", "uploads/photography/photo4.jpg"),
    ("Sony 24-70mm Lens", "uploads/photography/photo5.jpg"),
]

equipment = [
    ("Power Drill", "uploads/equipment/equipment1.jpg"),
    ("Concrete Mixer", "uploads/equipment/equipment2.jpg"),
    ("Portable Generator", "uploads/equipment/equipment3.jpg"),
    ("Welding Machine", "uploads/equipment/equipment4.jpg"),
    ("Pressure Washer", "uploads/equipment/equipment5.jpg"),
]

camping = [
    ("Camping Tent", "uploads/camping/camping1.jpg"),
    ("Sleeping Bag", "uploads/camping/camping2.jpg"),
    ("Camping Chair", "uploads/camping/camping3.jpg"),
    ("Portable Stove", "uploads/camping/camping4.jpg"),
    ("Hiking Backpack", "uploads/camping/camping5.jpg"),
]


def add_items(category, base_items, price_start):
    count = 0

    existing_count = db.query(Item).filter(Item.category == category).count()

    if existing_count > 0:
        print(f"{category} already has {existing_count} items. Skipping...")
        return

    for i in range(100):
        name, image = base_items[i % len(base_items)]
        location = locations[i % len(locations)]

        item = Item(
            title=f"{name} Rental - {location}",
            description=(
                f"{name} available for rent in {location}. "
                f"Suitable for daily rental use with affordable pricing."
            ),
            price_per_day=price_start + ((i % 10) * 50),
            location=location,
            image=image,
            category=category,
            approval_status="approved",
            owner_id=ADMIN_OWNER_ID,
        )

        db.add(item)
        count += 1

    db.commit()
    print(f"{count} {category} items added")


try:
    add_items("Vehicles", vehicles, 400)
    add_items("Photography", photography, 300)
    add_items("Equipment", equipment, 500)
    add_items("Camping", camping, 250)

    print("Extra category import completed successfully!")

except Exception as e:
    db.rollback()
    print("Import failed:", e)

finally:
    db.close()