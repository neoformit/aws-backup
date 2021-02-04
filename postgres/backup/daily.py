#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N days."""

from datetime import datetime, timedelta

from . import s3
from .config import DAILY_PREFIX, DAYS


def make():
    """Make the daily backup and clean up old backup files."""
    files = s3.read(contains=DAILY_PREFIX)
    print("Daily backup files currently in S3 storage:")
    for k, v in files.items():
        print(f'{k.ljust(30)} | {v.strftime("%Y-%m-%d %H:%M:%S")}')
    print()

    n_days_ago = datetime.now() - timedelta(days=DAYS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_days_ago
    }

    if old_files:
        print(
            "Removing old files from S3 storage:\n"
            + ' '.join(old_files.keys())
            + '\n'
        )
        for fname, timestamp in old_files.items():
            s3.remove(fname)
        print("Done")
    else:
        print("No old files to remove")
