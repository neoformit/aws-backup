#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N weeks."""

import os
import subprocess
from operator import itemgetter
from datetime import datetime, timedelta

WEEKS = 4
S3_PATH = 's3://neoform-backup/postgresql/'

DAILY_PREFIX = 'daily'
WEEKLY_PREFIX = 'weekly'
MONTHLY_PREFIX = 'monthly'


def read_s3(path):
    """Read files listed under given S3 bucket path and return stdout."""
    args = [
        'aws',
        's3',
        'ls',
        S3_PATH,
    ]
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def remove_from_s3(fname):
    """Remove specified filename from S3 storage under S3_PATH."""
    args = [
        'aws',
        's3',
        'rm',
        os.path.join(S3_PATH, fname),
    ]
    subprocess.run(args, check=True)


def s3_create_weekly_from_daily(files):
    """Copy lastest daily backup to convert to weekly backup."""
    daily_files = {
        k: v for k, v in files.items()
        if k.startswith(DAILY_PREFIX)
    }
    files_by_date = sorted(
        list(daily_files.items()),
        key=itemgetter(1),
        reverse=True,
    )
    newest = files_by_date[0][0]
    new_fname = newest.replace(DAILY_PREFIX, WEEKLY_PREFIX)
    args = [
        'aws',
        's3',
        'cp',
        os.path.join(S3_PATH, newest),
        os.path.join(S3_PATH, new_fname),
    ]
    subprocess.run(args, check=True)


files = {}
weekly_files = [
    x for x in read_s3(S3_PATH).split('\n')
    if x.startswith(WEEKLY_PREFIX)
]
for line in weekly_files:
    cols = [x for x in line.split(' ') if x]
    timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
    filename = cols[-1]
    files[filename] = timestamp

n_weeks_ago = datetime.now() - timedelta(weeks=WEEKS + 1)

old_files = {
    k: v for k, v in files.items()
    if v < n_weeks_ago
}

if old_files:
    s3_create_weekly_from_daily(files)

    print(
        f"Removing old files from S3 storage:\n{' '.join(old_files.keys())}\n"
    )

    for fname, timestamp in old_files.items():
        remove_from_s3(fname)

    print("Done")
else:
    print("No old files to remove")

