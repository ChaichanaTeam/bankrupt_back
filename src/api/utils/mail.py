import smtplib
from email.message import EmailMessage
from src.core.config import settings

class EmailServer:
    def __init__(self):
        self.smtp: smtplib.SMTP = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(settings.EMAIL, settings.EMAIL_PASSWORD)
    
    def send_message(self, msg: EmailMessage) -> None:
        self.smtp.send_message(msg)

    def __del__(self):
        self.smtp.quit()
    

email_service: EmailServer = EmailServer()

def send_verification_email(email: str, code: str) -> None:
    msg: EmailMessage = EmailMessage()
    msg["Subject"] = "Email verification"
    msg["From"] = settings.EMAIL
    msg["To"] = email

    msg.set_content(
        f"Hi!\n\nThis is your verification code: {code}"
    )

    try:
        email_service.send_message(msg)
    except Exception as e:
        print(f"Mail has not been sended: {e}")