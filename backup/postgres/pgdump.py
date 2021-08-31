"""Make postgres database dump."""

import datetime
import subprocess

from . import s3
from config import config, logger


def to_s3():
    """Make database dump with pg_dumpall."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    fname = f"daily_{today}.sql.gz"
    logger.info(f"Writing pg_dumpall to {fname}...")
    args = [
        'pg_dumpall',
        '|', 'gzip',
        '>', fname,
    ]
    subprocess.run(args, check=True)
    dest = os.path.join(config.S3_POSTGRES_PATH, fname)
    logger.info(f"Sending {fname} to {dest}...")
    s3.move(fname, dest)
