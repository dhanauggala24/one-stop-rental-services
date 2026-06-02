from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db_dependency import get_db
from app.models.cart_model import Cart
from app.models.item_model import Item
from app.schemas.cart_schema import CartCreate
from app.services.jwt_bearer import verify_token

router = APIRouter()


@router.post("/add-to-cart")
def add_to_cart(
    cart: CartCreate,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "user":
        raise HTTPException(
            status_code=403,
            detail="Only users can add items to cart"
        )

    item = db.query(Item).filter(
        Item.id == cart.item_id,
        Item.approval_status == "approved"
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found or not approved"
        )

    days = (cart.end_date - cart.start_date).days + 1

    if days <= 0:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    total_price = int(days * item.price_per_day)

    new_cart_item = Cart(
        user_id=user["user_id"],
        item_id=cart.item_id,
        start_date=cart.start_date,
        end_date=cart.end_date,
        total_price=total_price
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return {
        "message": "Item added to cart successfully",
        "cart_id": new_cart_item.id,
        "total_price": total_price
    }


@router.get("/my-cart")
def my_cart(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    cart_items = db.query(Cart, Item).join(
        Item,
        Cart.item_id == Item.id
    ).filter(
        Cart.user_id == user["user_id"]
    ).all()

    result = []

    for cart, item in cart_items:
        result.append({
            "cart_id": cart.id,
            "item_id": cart.item_id,
            "title": item.title,
            "description": item.description,
            "location": item.location,
            "category": item.category,
            "price_per_day": item.price_per_day,
            "image": item.image,
            "start_date": str(cart.start_date),
            "end_date": str(cart.end_date),
            "total_price": cart.total_price
        })

    return result


@router.delete("/remove-from-cart/{cart_id}")
def remove_from_cart(
    cart_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == user["user_id"]
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Item removed from cart"
    }