from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user_model import User
from app.services.jwt_bearer import verify_token

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/request-provider")
def request_provider(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    current_user = db.query(User).filter(
        User.id == user["user_id"]
    ).first()

    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.role == "provider":
        return {
            "message": "You are already a provider"
        }

    if current_user.provider_status == "pending":
        return {
            "message": "Provider request already pending"
        }

    current_user.provider_status = "pending"

    db.commit()

    return {
        "message": "Provider request submitted successfully"
    }


@router.get("/provider-requests")
def provider_requests(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can view provider requests"
        )

    requests = db.query(User).filter(
        User.provider_status == "pending"
    ).all()

    return requests


@router.put("/approve-provider/{user_id}")
def approve_provider(
    user_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can approve providers"
        )

    requested_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not requested_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    requested_user.role = "provider"
    requested_user.provider_status = "approved"

    db.commit()

    return {
        "message": "Provider approved successfully"
    }