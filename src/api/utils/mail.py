##
import smtplib
from email.message import EmailMessage

def send_verification_email(email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Email verification"
    msg["From"] = "#"
    msg["To"] = email
    msg.set_content(
        f"Hi!\n\nPlease, verify your email on this link:\n"
        f"http://localhost:8000/verify-email?token={token}"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("#", "#")
            server.send_message(msg)
    except Exception as e:
        print(f"Mail has not been sended: {e}")
##