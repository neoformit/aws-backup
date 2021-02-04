"""Send email to admin."""

import os
import smtplib
from dotenv import load_dotenv

load_dotenv()
port = 25
smtp_server = os.environ['EMAIL_HOSTNAME']
sender_email = os.environ['EMAIL_USERNAME']
password = os.environ['EMAIL_PASSWORD']
recipient_email = os.environ['EMAIL_RECIPIENT']


def send_mail(message):
    """Dispatch mail with given content and recipient(s)."""
    msg = (
        f"From: {sender_email}\n"
        f"To: {recipient_email}\n"
        f"Subject: Neoform PG backup error\n\n{message}"
    )

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg)
