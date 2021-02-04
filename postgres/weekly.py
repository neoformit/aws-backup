#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N weeks."""

import os
from operator import itemgetter
from datetime import datetime, timedelta

from . import s3
from config import WEEKS, DAILY_PREFIX, WEEKLY_PREFIX, S3_POSTGRES_PATH


def make():
    """Make weekly backup from daily backup file and remove old files."""
    create_weekly_from_daily()
    files = s3.read(contains=WEEKLY_PREFIX)
    n_weeks_ago = datetime.now() - timedelta(weeks=WEEKS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_weeks_ago
    }
    if old_files:
        print(
            "Removing old files from S3 storage:\n"
            + ' '.join(old_files.keys())
            + "\n"
        )
        for fname in old_files:
            s3.remove(fname)
        print("Done")
    else:
        print("No old files to remove")


def create_weekly_from_daily():
    """Copy lastest daily backup to convert to weekly backup."""
    daily_files = s3.read(contains=DAILY_PREFIX)
    if not daily_files:
        print("Can't make weekly backup, no daily backups yet.")
        return
    files_by_date = sorted(
        list(daily_files.items()),
        key=itemgetter(1),
    )
    oldest = files_by_date[0][0]
    new_fname = oldest.replace(DAILY_PREFIX, WEEKLY_PREFIX)
    print(f"Creating weekly backup file {new_fname} from daily file {oldest}")
    s3.copy(
        os.path.join(S3_POSTGRES_PATH, oldest),
        os.path.join(S3_POSTGRES_PATH, new_fname),
    )
