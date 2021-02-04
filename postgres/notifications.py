"""Send email to admin."""

import dotenv
import smtplib

port = 25
password =
smtp_server =
sender_email =
recipient_email =


def send_mail(message):
    """Dispatch mail with given content and recipient(s)."""
    # context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message)
