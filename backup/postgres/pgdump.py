"""Make postgres database dump."""

import os
import logging
import datetime
import subprocess

from . import s3
from config import config
from backup.utils import tmp

logger = logging.getLogger(__name__)


def to_s3():
    """Make database dump with pg_dumpall."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    fname = f"daily_{today}.sql.gz"
    fpath = tmp(fname)
    logger.info(f"Writing {config.DB_DUMP_CMD} to {fpath}...")

    with open(fpath, 'wb', 1) as stream:
        logger.debug(f"RUN: {config.DB_DUMP_CMD} | gzip > {fpath}")
        dump = subprocess.run(
            [config.DB_DUMP_CMD],
            check=True,
            stdout=subprocess.PIPE,
        )
        gzip = subprocess.run(
            ['gzip'],
            check=True,
            stdin=dump.stdout,
            stdout=stream,
        )
        gzip.wait()

    dest = os.path.join(config.S3_POSTGRES_PATH, fname)
    logger.info(f"Sending {fpath} to {dest}...")
    s3.move(fpath, dest)
