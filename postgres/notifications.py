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
    # context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message)
