import random
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

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

    body = f"""
One Stop Rental Services

Your password reset OTP is: {otp}

This OTP is valid for 10 minutes.
"""

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number
    )

    return message.sid  