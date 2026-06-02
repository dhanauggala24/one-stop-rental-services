from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import qrcode
import os

from app.database.db_dependency import get_db
from app.models.booking_model import Booking
from app.models.item_model import Item
from app.schemas.booking_schema import BookingCreate
from app.services.jwt_bearer import verify_token

router = APIRouter()


def check_booking_overlap(
    db: Session,
    item_id: int,
    start_date,
    end_date
):
    return db.query(Booking).filter(
        Booking.item_id == item_id,
        Booking.status.in_(["approved", "pending"]),
        Booking.start_date <= end_date,
        Booking.end_date >= start_date
    ).first()


@router.post("/book-item")
def book_item(
    booking: BookingCreate,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "user":
        raise HTTPException(
            status_code=403,
            detail="Only users can book items"
        )

    item = db.query(Item).filter(
        Item.id == booking.item_id,
        Item.approval_status == "approved"
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found or not approved"
        )

    if booking.start_date > booking.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    existing_booking = check_booking_overlap(
        db=db,
        item_id=booking.item_id,
        start_date=booking.start_date,
        end_date=booking.end_date
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Item already booked for selected dates"
        )

    new_booking = Booking(
        item_id=booking.item_id,
        renter_id=user["user_id"],
        start_date=booking.start_date,
        end_date=booking.end_date,
        status="pending"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "message": "Booking request created successfully",
        "booking_id": new_booking.id
    }


@router.get("/my-bookings")
def my_bookings(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking, Item).join(
        Item,
        Booking.item_id == Item.id
    ).filter(
        Booking.renter_id == user["user_id"]
    ).order_by(
        Booking.id.desc()
    ).limit(100).all()

    result = []

    for booking, item in bookings:
        result.append({
            "booking_id": booking.id,
            "item_id": booking.item_id,
            "item_title": item.title,
            "location": item.location,
            "price_per_day": item.price_per_day,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "status": booking.status
        })

    return result


@router.get("/provider-bookings")
def provider_bookings(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can access bookings"
        )

    bookings = db.query(Booking, Item).join(
        Item,
        Booking.item_id == Item.id
    ).order_by(
        Booking.id.desc()
    ).limit(100).all()

    result = []

    for booking, item in bookings:
        result.append({
            "booking_id": booking.id,
            "item_id": booking.item_id,
            "item_title": item.title,
            "location": item.location,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "status": booking.status
        })

    return result


@router.put("/update-booking-status/{booking_id}")
def update_booking_status(
    booking_id: int,
    status: str,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can update bookings"
        )

    allowed_status = ["approved", "rejected", "pending"]

    if status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if status == "approved":
        existing_booking = db.query(Booking).filter(
            Booking.id != booking.id,
            Booking.item_id == booking.item_id,
            Booking.status == "approved",
            Booking.start_date <= booking.end_date,
            Booking.end_date >= booking.start_date
        ).first()

        if existing_booking:
            raise HTTPException(
                status_code=400,
                detail="Cannot approve. Item already booked for selected dates"
            )

    booking.status = status
    db.commit()

    return {
        "message": f"Booking {status} successfully"
    }


@router.delete("/cancel-booking/{booking_id}")
def cancel_booking(
    booking_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.renter_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can cancel only your bookings"
        )

    db.delete(booking)
    db.commit()

    return {
        "message": "Booking cancelled successfully"
    }


@router.get("/booking-qr/{booking_id}")
def generate_booking_qr(
    booking_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.renter_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can access only your bookings"
        )

    item = db.query(Item).filter(
        Item.id == booking.item_id
    ).first()

    item_title = item.title if item else str(booking.item_id)

    os.makedirs("qr_codes", exist_ok=True)

    qr_data = f"""
ONE STOP RENTAL SERVICES BOOKING

Booking ID: {booking.id}
Item: {item_title}
Renter ID: {booking.renter_id}
Status: {booking.status}
Start Date: {booking.start_date}
End Date: {booking.end_date}
"""

    qr = qrcode.make(qr_data)

    file_path = f"qr_codes/booking_{booking.id}.png"

    qr.save(file_path)

    return {
        "message": "QR Code generated successfully",
        "qr_path": file_path
    }


@router.get("/booking-receipt/{booking_id}")
def booking_receipt(
    booking_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.renter_id != user["user_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can access only your bookings"
        )

    item = db.query(Item).filter(
        Item.id == booking.item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "booking_id": booking.id,
        "item_id": booking.item_id,
        "item_title": item.title,
        "location": item.location,
        "price_per_day": item.price_per_day,
        "start_date": booking.start_date,
        "end_date": booking.end_date,
        "status": booking.status
    }