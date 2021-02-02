#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N months."""

import os
import subprocess
from operator import itemgetter
from datetime import datetime, timedelta

MONTHS = 6
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
    result = subprocess.run(args, stdout=subprocess.PIPE, check=True)
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


def s3_create_monthly_from_weekly(files):
    """Copy lastest weekly backup to convert to monthly backup."""
    weekly_files = {
        k: v for k, v in files.items()
        if k.startswith(WEEKLY_PREFIX)
    }
    files_by_date = sorted(
        list(weekly_files.items()),
        key=itemgetter(1),
        reverse=True,
    )
    newest = files_by_date[0][0]
    print(f'Creating monthly backup from {newest}')
    new_fname = newest.replace(WEEKLY_PREFIX, MONTHLY_PREFIX)
    args = [
        'aws',
        's3',
        'cp',
        os.path.join(S3_PATH, newest),
        os.path.join(S3_PATH, new_fname),
    ]
    subprocess.run(args, check=True)


files = {}
monthly_files = [
    x for x in read_s3(S3_PATH).split('\n')
    if x.startswith(MONTHLY_PREFIX)
]

for line in monthly_files:
    cols = [x for x in line.split(' ') if x]
    timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
    filename = cols[-1]
    files[filename] = timestamp

n_months_ago = datetime.now() - timedelta(days=MONTHS + 1)

old_files = {
    k: v for k, v in files.items()
    if v < n_months_ago
}

if old_files:
    s3_create_monthly_from_weekly(files)

    print(
        f"Removing old files from S3 storage:\n{' '.join(old_files.keys())}\n"
    )

    for fname, timestamp in old_files.items():
        remove_from_s3(fname)

    print("Done")
else:
    print("No old files to remove")
