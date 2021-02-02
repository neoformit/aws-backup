"""Back up tar archives to AWS S3 and clean up old files."""

import s3
from datetime import date
from operator import itemgetter

DAILY_PREFIX = 'daily'
WEEKLY_PREFIX = 'weekly'
MONTHLY_PREFIX = 'monthly'

# Number of records to retain:
DAILY_RECORDS = 7
WEEKLY_RECORDS = 3
MONTHLY_RECORDS = 5


def to_s3_storage(archives):
    """Send newly created archives to s3 storage."""
    s3.store(archives)


def cleanup():
    """Run all cleanup operations to organise s3 backup archives."""
    today = date.today()
    if today.day == 1:
        monthly_cleanup()
    if today.weekday() == 0:
        weekly_cleanup()
    daily_cleanup()


def monthly_cleanup():
    """Move and delete backups to retain monthly backup archives."""
    s3_files = s3.read_files()

    weekly = sorted([
        (f, m) for f, m in s3_files
        if f.startswith(WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    monthly = sorted([
        (f, m) for f, m in s3_files
        if f.startswith(MONTHLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if weekly[0][1] > monthly[0][1]:
        new_fpath = weekly[0][0].replace(WEEKLY_PREFIX, MONTHLY_PREFIX, 1)
        s3.copy(
            weekly[0][0],
            new_fpath
        )
        monthly.insert(new_fpath, 0)

    if len(monthly) > MONTHLY_RECORDS:
        oldest = monthly[MONTHLY_RECORDS:]
        for f in oldest:
            s3.remove(f)


def weekly_cleanup():
    """Move and delete backups to retain weekly backup archives."""
    s3_files = s3.read_files()

    daily = sorted([
        (f, m) for f, m in s3_files
        if f.startswith(DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    weekly = sorted([
        (f, m) for f, m in s3_files
        if f.startswith(WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if daily[0][1] > weekly[0][1]:
        new_fpath = daily[0][0].replace(DAILY_PREFIX, WEEKLY_PREFIX, 1)
        s3.copy(
            daily[0][0],
            new_fpath
        )
        weekly.insert(new_fpath, 0)

    if len(weekly) > WEEKLY_RECORDS:
        oldest = weekly[WEEKLY_RECORDS:]
        for f in oldest:
            s3.remove(f)


def daily_cleanup():
    """Move and delete backups to retain daily backup archives."""
    s3_files = s3.read_files()

    daily = sorted([
        (f, m) for f, m in s3_files
        if f.startswith(DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if len(daily) > DAILY_RECORDS:
        oldest = daily[DAILY_RECORDS:]
        for f in oldest:
            s3.remove(f)
