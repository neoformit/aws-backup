"""Send email to admin."""

import ssl
import smtplib

port = 587
password = None
smtp_server = "localhost"
sender_email = "dev@neoformit.com"
recipient_email = "chyde@neoformit.com"


def send_mail(message):
    """Dispatch mail with given content and recipient(s)."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message)
