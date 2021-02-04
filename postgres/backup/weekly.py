#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N weeks."""

import os
from operator import itemgetter
from datetime import datetime, timedelta

import s3
from config import WEEKS, DAILY_PREFIX, WEEKLY_PREFIX, S3_PATH


def make():
    """Make weekly backup from daily backup file and remove old files."""
    files = s3.read(contains=WEEKLY_PREFIX)
    n_weeks_ago = datetime.now() - timedelta(weeks=WEEKS + 1)
    old_files = {
        k: v for k, v in files.items()
        if v < n_weeks_ago
    }
    if old_files:
        create_weekly_from_daily(files)
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


def create_weekly_from_daily(files):
    """Copy lastest daily backup to convert to weekly backup."""
    daily_files = s3.read(contains=DAILY_PREFIX)
    files_by_date = sorted(
        list(daily_files.items()),
        key=itemgetter(1),
        reverse=True,
    )
    newest = files_by_date[0][0]
    new_fname = newest.replace(DAILY_PREFIX, WEEKLY_PREFIX)
    s3.copy(
        os.path.join(S3_PATH, newest),
        os.path.join(S3_PATH, new_fname),
    )
