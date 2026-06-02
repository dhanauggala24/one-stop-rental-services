import smtplib
import random
import os
import requests
from dotenv import load_dotenv
from email.message import EmailMessage
from datetime import datetime, timedelta

load_dotenv()

otp_storage = {}

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_SSL_PORT = int(os.getenv("SMTP_SSL_PORT", "465"))


def generate_otp():
    return str(random.randint(100000, 999999))


def _send_email_via_sendgrid(msg: EmailMessage):
    if not SENDGRID_API_KEY:
        raise Exception("SendGrid API key not configured")

    payload = {
        "personalizations": [
            {
                "to": [{"email": msg["To"]}],
                "subject": msg["Subject"],
            }
        ],
        "from": {"email": msg["From"]},
        "content": [
            {
                "type": "text/plain",
                "value": msg.get_content(),
            }
        ],
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        json=payload,
        headers=headers,
        timeout=15,
    )

    if response.status_code >= 300:
        raise Exception(
            f"SendGrid error {response.status_code}: {response.text}"
        )


def _send_email_via_smtp(msg: EmailMessage):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise Exception("SMTP credentials not configured")

    last_error = None
    for use_ssl, port in ((True, SMTP_SSL_PORT), (False, SMTP_PORT)):
        try:
            if use_ssl:
                with smtplib.SMTP_SSL(SMTP_HOST, port, timeout=15) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
                    smtp.send_message(msg)
                    return
            else:
                with smtplib.SMTP(SMTP_HOST, port, timeout=15) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
                    smtp.send_message(msg)
                    return
        except Exception as exc:
            last_error = exc

    raise Exception(
        f"Unable to send OTP email via SMTP {SMTP_HOST}. Last error: {last_error}"
    )


def _send_email_message(msg: EmailMessage):
    if SENDGRID_API_KEY:
        try:
            _send_email_via_sendgrid(msg)
            return
        except Exception:
            # If SendGrid fails, fall back to SMTP if credentials are available.
            pass

    _send_email_via_smtp(msg)


def send_otp_email(receiver_email: str, otp: str):
    if not SENDGRID_API_KEY and (not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD):
        raise Exception("No email transport configured. Set SENDGRID_API_KEY or SMTP credentials.")

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP - One Stop Rental Services"
    msg["From"] = EMAIL_ADDRESS or os.getenv("EMAIL_ADDRESS")
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

    _send_email_message(msg)


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