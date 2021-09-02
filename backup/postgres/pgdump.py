"""Make postgres database dump."""

import os
import logging
import datetime
import subprocess

from . import s3
from config import config
from backup.utils import tmp
from backup.notifications import send_mail

logger = logging.getLogger(__name__)


def to_s3():
    """Make database dump with pg_dumpall."""
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        fname = f"daily_{today}.sql.gz"
        fpath = tmp(fname)
        logger.info(f"Writing {config.DB_DUMP_CMD} to {fpath}...")
        logger.debug(
            f"RUN:\n\t$sudo -u postgres {config.DB_DUMP_CMD} | gzip > {fpath}")

        dump = subprocess.Popen(
            ['sudo', '-u', 'postgres', config.DB_DUMP_CMD],
            stdout=subprocess.PIPE,
        )

        with open(fpath, 'wb') as stream:
            subprocess.run(
                ['gzip'],
                check=True,
                stdin=dump.stdout,
                stdout=stream,
            )

        dest = os.path.join(config.S3_POSTGRES_PATH, fname)
        logger.info(f"Sending {fpath} to {dest}...")
        s3.move(fpath, dest)
    except Exception as exc:
        send_mail('Error encountered making DB cascade:', error=True)
        raise exc
