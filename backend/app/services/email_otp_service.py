import random
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

otp_storage = {}

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")


def generate_otp():
    return str(random.randint(100000, 999999))


def format_whatsapp_number(phone_number: str):
    phone = str(phone_number).strip().replace(" ", "").replace("-", "")

    if phone.startswith("whatsapp:"):
        return phone

    if phone.startswith("+"):
        return f"whatsapp:{phone}"

    if len(phone) == 10:
        return f"whatsapp:+91{phone}"

    if phone.startswith("91") and len(phone) == 12:
        return f"whatsapp:+{phone}"

    return f"whatsapp:+{phone}"


def send_otp_whatsapp(phone_number: str, otp: str):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_NUMBER:
        raise Exception("Twilio credentials not configured")

    from_number = TWILIO_WHATSAPP_NUMBER

    if not from_number.startswith("whatsapp:"):
        from_number = f"whatsapp:{from_number}"

    to_number = format_whatsapp_number(phone_number)

    message_body = f"""
One Stop Rental Services

Your password reset OTP is: {otp}

This OTP is valid for 10 minutes.
"""

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        return message.sid

    except Exception as e:
        raise Exception(f"WhatsApp OTP sending failed: {str(e)}")


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