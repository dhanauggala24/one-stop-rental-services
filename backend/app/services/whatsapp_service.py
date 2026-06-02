import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER",
    "whatsapp:+14155238886"
)


def format_whatsapp_number(phone_number: str):
    phone_number = str(phone_number).strip()

    if phone_number.startswith("whatsapp:"):
        return phone_number

    if phone_number.startswith("+"):
        return f"whatsapp:{phone_number}"

    if len(phone_number) == 10:
        return f"whatsapp:+91{phone_number}"

    return f"whatsapp:+{phone_number}"


def send_whatsapp_message(phone_number: str, message: str):
    try:
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            return {
                "status": "failed",
                "error": "Twilio credentials are missing in .env"
            }

        client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=format_whatsapp_number(phone_number)
        )

        return {
            "status": "success",
            "sid": msg.sid,
            "message_status": msg.status
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }