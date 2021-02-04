"""Send email to admin."""

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate


def send_mail(to, frm, subject, body, server="localhost"):
    """Dispatch mail with given content and recipient(s)."""
    assert type(to) == list

    msg = MIMEMultipart()
    msg['From'] = frm
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(frm, to, msg.as_string())
    smtp.close()
