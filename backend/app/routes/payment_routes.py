from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import qrcode
import os

from app.database.db_dependency import get_db
from app.models.cart_model import Cart
from app.models.booking_model import Booking
from app.models.item_model import Item
from app.models.user_model import User
from app.services.jwt_bearer import verify_token
from app.services.whatsapp_service import send_whatsapp_message

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


@router.get("/test-whatsapp")
def test_whatsapp():
    result = send_whatsapp_message(
        "919848697246",
        "Hello Dhana! WhatsApp integration is working successfully."
    )

    return result


@router.post("/confirm-payment")
def confirm_payment(
    background_tasks: BackgroundTasks,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "user":
        raise HTTPException(
            status_code=403,
            detail="Only users can make payment"
        )

    current_user = db.query(User).filter(
        User.id == user["user_id"]
    ).first()

    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not current_user.phone_number:
        raise HTTPException(
            status_code=400,
            detail="User phone number not found"
        )

    cart_items = db.query(Cart, Item).join(
        Item,
        Cart.item_id == Item.id
    ).filter(
        Cart.user_id == user["user_id"]
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    created_bookings = []
    receipt_items = []
    total_amount = 0

    try:
        for cart, item in cart_items:
            if cart.start_date > cart.end_date:
                raise HTTPException(
                    status_code=400,
                    detail="Start date cannot be after end date"
                )

            existing_booking = check_booking_overlap(
                db=db,
                item_id=cart.item_id,
                start_date=cart.start_date,
                end_date=cart.end_date
            )

            if existing_booking:
                raise HTTPException(
                    status_code=400,
                    detail=f"{item.title} is already booked for selected dates"
                )

            new_booking = Booking(
                item_id=cart.item_id,
                renter_id=user["user_id"],
                start_date=cart.start_date,
                end_date=cart.end_date,
                status="approved"
            )

            db.add(new_booking)
            db.flush()

            created_bookings.append(new_booking.id)
            total_amount += cart.total_price

            receipt_items.append({
                "booking_id": new_booking.id,
                "item_name": item.title,
                "location": item.location,
                "start_date": str(cart.start_date),
                "end_date": str(cart.end_date),
                "price_per_day": item.price_per_day,
                "total_price": cart.total_price
            })

        os.makedirs("qr_codes", exist_ok=True)

        qr_text = "ONE STOP RENTAL SERVICES PAYMENT RECEIPT\n"
        qr_text += "----------------------------------------\n"
        qr_text += f"User Name: {current_user.name}\n"
        qr_text += f"Email: {current_user.email}\n"
        qr_text += f"Phone: {current_user.phone_number}\n"
        qr_text += f"Total Amount Paid: Rs.{total_amount}\n"
        qr_text += "Payment Status: Successful\n\n"
        qr_text += "Booked Items:\n"

        for booked_item in receipt_items:
            qr_text += (
                f"\nBooking ID: {booked_item['booking_id']}\n"
                f"Item: {booked_item['item_name']}\n"
                f"Location: {booked_item['location']}\n"
                f"From: {booked_item['start_date']}\n"
                f"To: {booked_item['end_date']}\n"
                f"Price/Day: Rs.{booked_item['price_per_day']}\n"
                f"Total: Rs.{booked_item['total_price']}\n"
            )

        qr_path = f"qr_codes/payment_receipt_user_{user['user_id']}.png"
        qr = qrcode.make(qr_text)
        qr.save(qr_path)

        for cart, item in cart_items:
            db.delete(cart)

        user_name = current_user.name
        user_email = current_user.email
        user_phone = current_user.phone_number

        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Payment failed: {str(e)}"
        )

    booked_items_text = ""

    for booked_item in receipt_items:
        booked_items_text += (
            f"\nBooking ID: {booked_item['booking_id']}\n"
            f"Item: {booked_item['item_name']}\n"
            f"Slot: {booked_item['start_date']} to {booked_item['end_date']}\n"
            f"Amount: Rs.{booked_item['total_price']}\n"
        )

    whatsapp_message = (
        f"ONE STOP RENTAL SERVICES\n\n"
        f"Payment Successful ✅\n\n"
        f"Name: {user_name}\n"
        f"Email: {user_email}\n"
        f"Phone: {user_phone}\n"
        f"Total Amount Paid: Rs.{total_amount}\n\n"
        f"Booked Items:\n"
        f"{booked_items_text}\n"
        f"Thank you for using One Stop Rental Services."
    )

    background_tasks.add_task(
        send_whatsapp_message,
        user_phone,
        whatsapp_message
    )

    return {
        "message": "Payment successful",
        "booking_ids": created_bookings,
        "receipt": {
            "user_name": user_name,
            "email": user_email,
            "phone_number": user_phone,
            "items": receipt_items,
            "total_amount": total_amount,
            "payment_status": "successful"
        },
        "qr_path": qr_path,
        "whatsapp_message": whatsapp_message
    }