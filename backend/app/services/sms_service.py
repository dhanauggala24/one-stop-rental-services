import os
import requests
from dotenv import load_dotenv

load_dotenv()

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")


def send_payment_sms(phone_number: str, message: str):

    if not FAST2SMS_API_KEY:
        return {
            "success": False,
            "message": "FAST2SMS_API_KEY missing in .env"
        }

    if not phone_number:
        return {
            "success": False,
            "message": "Phone number missing"
        }

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "authorization": FAST2SMS_API_KEY,
        "route": "q",
        "message": message,
        "numbers": phone_number,
    }

    try:
        response = requests.get(url, params=payload)

        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json()
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }