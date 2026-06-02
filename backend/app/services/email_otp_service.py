import smtplib
import random
import os
from email.message import EmailMessage
from datetime import datetime, timedelta

otp_storage = {}


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(receiver_email: str, otp: str):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise Exception("Email credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP - One Stop Rental Services"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 10 minutes.

Regards,
One Stop Rental Services
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def save_otp(email: str, otp: str):
    otp_storage[email] = {
        "otp": otp,
        "expires_at": datetime.now() + timedelta(minutes=10),
        "verified": False
    }


def verify_otp(email: str, otp: str):
    data = otp_storage.get(email)

    if not data:
        return False

    if datetime.now() > data["expires_at"]:
        otp_storage.pop(email, None)
        return False

    if data["otp"] != otp:
        return False

    data["verified"] = True
    return True


def is_otp_verified(email: str):
    data = otp_storage.get(email)
    return data and data.get("verified") is True


def clear_otp(email: str):
    otp_storage.pop(email, None)