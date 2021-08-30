#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N months."""

import os
from operator import itemgetter
from datetime import datetime, timedelta

from . import s3
from config import WEEKLY_PREFIX, MONTHLY_PREFIX, MONTHS, S3_POSTGRES_PATH


def make():
    """Make monthly backup from weekly backup files and remove old files."""
    files = s3.read(contains=MONTHLY_PREFIX)
    print("Monthly backup files currently in S3 storage:")
    for k, v in files.items():
        print(f'{k.ljust(30)} | {v.strftime("%Y-%m-%d %H:%M:%S")}')
    if files:
        print()
    else:
        print("None")

    create_monthly_from_weekly()

    n_months_ago = datetime.now() - timedelta(days=MONTHS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_months_ago
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


def create_monthly_from_weekly():
    """Copy lastest weekly backup to convert to monthly backup."""
    weekly_files = s3.read(contains=WEEKLY_PREFIX)
    if not weekly_files:
        print("Can't make monthly backup, no weekly backups yet.")
        return
    files_by_date = sorted(
        list(weekly_files.items()),
        key=itemgetter(1),
    )
    oldest = files_by_date[0][0]
    new_fname = oldest.replace(WEEKLY_PREFIX, MONTHLY_PREFIX)
    print(f'Creating monthly backup file {new_fname} from weekly backup {oldest}')
    s3.copy(
        os.path.join(S3_POSTGRES_PATH, oldest),
        os.path.join(S3_POSTGRES_PATH, new_fname),
    )
