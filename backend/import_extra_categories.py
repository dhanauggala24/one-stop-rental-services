from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.item_model import Item
from app.models.user_model import User

db: Session = SessionLocal()

ADMIN_OWNER_ID = 4

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
    "Honda Activa",
    "TVS Jupiter",
    "Royal Enfield Classic 350",
    "Bajaj Pulsar",
    "Yamaha FZ",
    "Maruti Swift",
    "Hyundai i20",
    "Tata Nexon",
    "Mahindra Thar",
    "Toyota Innova",
]

photography = [
    "Canon EOS 1500D",
    "Nikon D5600",
    "Sony Alpha A6400",
    "Canon 50mm Lens",
    "Sony 24-70mm Lens",
    "DJI Mini Drone",
    "GoPro Hero 12",
    "Tripod Stand",
    "Ring Light Kit",
    "Studio Lighting Kit",
]

equipment = [
    "Power Drill",
    "Concrete Mixer",
    "Portable Generator",
    "Welding Machine",
    "Pressure Washer",
    "Ladder",
    "Water Pump",
    "Grass Cutter",
    "Projector",
    "Sound System",
]

camping = [
    "Camping Tent",
    "Sleeping Bag",
    "Camping Chair",
    "Portable Stove",
    "Hiking Backpack",
    "LED Lantern",
    "Trekking Poles",
    "Cooler Box",
    "Camping Table",
    "First Aid Kit",
]


def add_items(category, base_items, price_start):
    count = 0

    for i in range(100):
        name = base_items[i % len(base_items)]
        location = locations[i % len(locations)]

        title = f"{name} Rental - {location}"

        description = (
            f"{name} available for rent in {location}. "
            f"Suitable for daily rental use with affordable pricing."
        )

        price = price_start + ((i % 10) * 50)

        item = Item(
            title=title,
            description=description,
            price_per_day=price,
            location=location,
            category=category,
            approval_status="approved",
            owner_id=ADMIN_OWNER_ID,
        )

        db.add(item)
        count += 1

    print(f"{count} {category} items added")


add_items("Vehicles", vehicles, 400)
add_items("Photography", photography, 300)
add_items("Equipment", equipment, 500)
add_items("Camping", camping, 250)

db.commit()
db.close()

print("Extra category import completed successfully!")