"""Send email to admin."""

import os
import smtplib
import logging
from config import config

logger = logging.getLogger(__name__)

PORT = 25
HOST = config.EMAIL_HOSTNAME
PASSWORD = config.EMAIL_PASSWORD
SENDER_EMAIL = config.EMAIL_USERNAME
RECIPIENT_EMAIL = config.EMAIL_RECIPIENT


def send_mail(message):
    """Dispatch mail with given content and recipient(s)."""
    msg = (
        f"From: {SENDER_EMAIL}\n"
        f"To: {RECIPIENT_EMAIL}\n"
        f"Subject: Neoform PG backup error\n\n{message}"
    )

    if not (
            HOST
            and PASSWORD
            and SENDER_EMAIL
            and RECIPIENT_EMAIL) or os.environ.get('DRY_RUN'):
        logger.info("Dummy email\n" + 80 * "-" + '\n' + msg)
        return

    with smtplib.SMTP(HOST, PORT) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg)
