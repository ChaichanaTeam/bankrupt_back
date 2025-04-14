import smtplib
from email.message import EmailMessage
from src.core.config import settings

smpt_server = smtplib.SMTP("smtp.gmail.com", 587)
smpt_server.starttls()
smpt_server.login(settings.EMAIL, settings.EMAIL_PASSWORD)

def send_verification_email(email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Email verification"
    msg["From"] = settings.EMAIL
    msg["To"] = email

    msg.set_content(
        f"Hi!\n\nPlease, verify your email on this link:\n"
        f"http://localhost:8000/verify-email?token={token}"
    )

    try:
            smpt_server.send_message(msg)
    except Exception as e:
        print(f"Mail has not been sended: {e}")