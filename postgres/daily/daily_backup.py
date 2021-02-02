#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N days."""

import os
import subprocess
from datetime import datetime, timedelta

DAILY_PREFIX = 'daily'
WEEKLY_PREFIX = 'weekly'
MONTHLY_PREFIX = 'monthly'

DAYS = 7
S3_PATH = 's3://neoform-backup/postgresql/'


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


# Set pwd
os.chdir('/mnt/vdisk/postgresql/backup/daily/')

files = {}
daily_files = [
    x for x in read_s3(S3_PATH).split('\n')
    if x.startswith(DAILY_PREFIX)
]

for line in daily_files:
    cols = [x for x in line.split(' ') if x]
    timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
    filename = cols[-1]
    files[filename] = timestamp

print("Files currently in S3 storage:")
for k, v in files.items():
    print(f'{k.ljust(30)} | {v.strftime("%Y-%m-%d %H:%M:%S")}')
print()

n_days_ago = datetime.now() - timedelta(days=DAYS + 1)

old_files = {
    k: v for k, v in files.items()
    if v < n_days_ago
}

if old_files:
    print(
        f"Removing old files from S3 storage:\n{' '.join(old_files.keys())}\n"
    )

    for fname, timestamp in old_files.items():
        remove_from_s3(fname)

    print("Done")
else:
    print("No old files to remove")
