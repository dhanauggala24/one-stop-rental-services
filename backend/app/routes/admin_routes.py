from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user_model import User
from app.models.item_model import Item
from app.models.booking_model import Booking
from app.services.jwt_bearer import verify_token

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def check_admin(user):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can access this"
        )


@router.get("/admin-dashboard")
def admin_dashboard(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    check_admin(user)

    total_users = db.query(User).count()
    total_items = db.query(Item).count()
    total_bookings = db.query(Booking).count()

    pending_bookings = db.query(Booking).filter(
        Booking.status == "pending"
    ).count()

    approved_bookings = db.query(Booking).filter(
        Booking.status == "approved"
    ).count()

    rejected_bookings = db.query(Booking).filter(
        Booking.status == "rejected"
    ).count()

    pending_items = db.query(Item).filter(
        Item.approval_status == "pending"
    ).count()

    approved_items = db.query(Item).filter(
        Item.approval_status == "approved"
    ).count()

    rejected_items = db.query(Item).filter(
        Item.approval_status == "rejected"
    ).count()

    bookings = db.query(Booking).order_by(
        Booking.id.desc()
    ).all()

    booking_details = []

    for booking in bookings:

        item = db.query(Item).filter(
            Item.id == booking.item_id
        ).first()

        renter = db.query(User).filter(
            User.id == booking.renter_id
        ).first()

        item_owner = None

        if item:
            item_owner = db.query(User).filter(
                User.id == item.owner_id
            ).first()

        price_per_day = item.price_per_day if item else 0

        days = (
            (booking.end_date - booking.start_date).days + 1
        )

        total_cost = price_per_day * days

        booking_details.append({
            "booking_id": booking.id,
            "item_owner_name": item_owner.name if item_owner else "Unknown",
            "user_name": renter.name if renter else "Unknown",
            "item_name": item.title if item else "Unknown",
            "start_date": str(booking.start_date),
            "end_date": str(booking.end_date),
            "price_per_day": price_per_day,
            "total_cost": total_cost,
            "status": booking.status
        })

    return {
        "total_users": total_users,
        "total_items": total_items,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "approved_bookings": approved_bookings,
        "rejected_bookings": rejected_bookings,
        "pending_items": pending_items,
        "approved_items": approved_items,
        "rejected_items": rejected_items,
        "bookings": booking_details
    }


@router.get("/pending-items")
def get_pending_items(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    check_admin(user)

    items = db.query(Item).filter(
        Item.approval_status == "pending"
    ).order_by(
        Item.id.desc()
    ).all()

    result = []

    for item in items:

        owner = db.query(User).filter(
            User.id == item.owner_id
        ).first()

        result.append({
            "item_id": item.id,
            "title": item.title,
            "description": item.description,
            "price_per_day": item.price_per_day,
            "location": item.location,
            "category": item.category,
            "image": item.image,
            "approval_status": item.approval_status,
            "owner_name": owner.name if owner else "Unknown",
            "owner_email": owner.email if owner else "Unknown"
        })

    return result


@router.put("/approve-item/{item_id}")
def approve_item(
    item_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    check_admin(user)

    item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item.approval_status = "approved"

    db.commit()
    db.refresh(item)

    return {
        "message": "Item approved successfully",
        "item_id": item.id
    }


@router.put("/reject-item/{item_id}")
def reject_item(
    item_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    check_admin(user)

    item = db.query(Item).filter(
        Item.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item.approval_status = "rejected"

    db.commit()
    db.refresh(item)

    return {
        "message": "Item rejected successfully",
        "item_id": item.id
    }