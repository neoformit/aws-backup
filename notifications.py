"""Send email to admin."""

import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
PORT = 25
HOST = os.environ['EMAIL_HOSTNAME']
PASSWORD = os.environ['EMAIL_PASSWORD']
SENDER_EMAIL = os.environ['EMAIL_USERNAME']
RECIPIENT_EMAIL = os.environ['EMAIL_RECIPIENT']


def send_mail(message):
    """Dispatch mail with given content and recipient(s)."""
    msg = (
        f"From: {SENDER_EMAIL}\n"
        f"To: {RECIPIENT_EMAIL}\n"
        f"Subject: Neoform PG backup error\n\n{message}"
    )

    with smtplib.SMTP(HOST, PORT) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg)
