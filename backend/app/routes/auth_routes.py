from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db_dependency import get_db
from app.models.user_model import User
from app.models.otp_model import OTP
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest
)
from app.services.hash_service import hash_password, verify_password
from app.services.jwt_service import create_access_token
from app.services.email_otp_service import generate_otp, send_otp_whatsapp

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Role must be user or admin")

    new_user = User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        password=hash_password(user.password),
        role=user.role,
        provider_status="not_requested"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": existing_user.id,
        "email": existing_user.email,
        "role": existing_user.role
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not registered")

    if not existing_user.phone_number:
        raise HTTPException(
            status_code=400,
            detail="Phone number not registered for this account"
        )

    otp_code = generate_otp()

    old_otps = db.query(OTP).filter(OTP.email == request.email).all()

    for old_otp in old_otps:
        db.delete(old_otp)

    new_otp = OTP(
        email=request.email,
        otp=otp_code,
        expires_at=OTP.expiry_time(),
        verified=False
    )

    db.add(new_otp)
    db.commit()

    send_otp_whatsapp(existing_user.phone_number, otp_code)

    return {
        "message": "OTP sent successfully to registered WhatsApp number"
    }


@router.post("/verify-otp")
def verify_password_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    otp_record = db.query(OTP).filter(
        OTP.email == request.email,
        OTP.otp == request.otp
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if datetime.now() > otp_record.expires_at:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    otp_record.verified = True
    db.commit()

    return {
        "message": "OTP verified successfully"
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    otp_record = db.query(OTP).filter(
        OTP.email == request.email,
        OTP.verified == True
    ).first()

    if not otp_record:
        raise HTTPException(
            status_code=400,
            detail="OTP verification required"
        )

    existing_user = db.query(User).filter(User.email == request.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.password = hash_password(request.new_password)

    db.delete(otp_record)
    db.commit()

    return {
        "message": "Password reset successfully"
    }