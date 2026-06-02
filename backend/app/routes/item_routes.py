from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os

from app.database.db_dependency import get_db
from app.models.item_model import Item
from app.models.booking_model import Booking
from app.schemas.item_schema import ItemCreate
from app.services.jwt_bearer import verify_token

router = APIRouter()


@router.post("/create-item")
def create_item(
    item: ItemCreate,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    new_item = Item(
        title=item.title,
        description=item.description,
        price_per_day=item.price_per_day,
        location=item.location,
        category=item.category,
        approval_status="pending",
        owner_id=user["user_id"]
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "message": "Item created successfully",
        "item_id": new_item.id
    }


@router.get("/all-items")
def get_all_items(
    db: Session = Depends(get_db)
):
    items = db.query(Item).filter(
        Item.approval_status == "approved"
    ).limit(100).all()

    return items


@router.get("/search-items")
def search_items(
    location: str = Query(...),
    db: Session = Depends(get_db)
):
    items = db.query(Item).filter(
        Item.location.ilike(f"%{location}%"),
        Item.approval_status == "approved"
    ).limit(100).all()

    return items


@router.get("/my-items")
def get_my_items(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    items = db.query(Item).filter(
        Item.owner_id == user["user_id"]
    ).limit(100).all()

    return items


@router.put("/update-item/{item_id}")
def update_item(
    item_id: int,
    item: ItemCreate,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    existing_item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if existing_item.owner_id != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can update only your own items"
        )

    existing_item.title = item.title
    existing_item.description = item.description
    existing_item.price_per_day = item.price_per_day
    existing_item.location = item.location
    existing_item.category = item.category

    db.commit()
    db.refresh(existing_item)

    return {
        "message": "Item updated successfully",
        "item": existing_item
    }


@router.delete("/delete-item/{item_id}")
def delete_item(
    item_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if item.owner_id != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can delete only your own items"
        )

    bookings = db.query(Booking).filter(
        Booking.item_id == item_id
    ).all()

    for booking in bookings:
        db.delete(booking)

    db.delete(item)
    db.commit()

    return {
        "message": "Item deleted successfully"
    }


@router.post("/upload-item-image/{item_id}")
def upload_item_image(
    item_id: int,
    file: UploadFile = File(...),
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if item.owner_id != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can upload image only for your own item"
        )

    os.makedirs("uploads", exist_ok=True)

    filename = f"{item_id}_{file.filename}"
    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    item.image = filepath
    db.commit()

    return {
        "message": "Image uploaded successfully",
        "image_path": filepath
    }