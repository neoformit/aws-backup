"""Back up tar archives to AWS S3 and clean up old files."""

import logging
from datetime import date
from operator import itemgetter

from config import config

from . import s3

logger = logging.getLogger(__name__)


def cascade():
    """Run all cleanup operations to organise s3 backup archives."""
    today = date.today()
    if today.day == config.MONTHLY_BACKUP_DAY:
        logger.info(f"Month day {today.day}: PERFORMING MONTHLY CASCADE")
        monthly_cleanup()
    if today.weekday() == config.WEEKLY_BACKUP_WEEKDAY:
        logger.info(f"Week day {today.weekday()}: PERFORMING WEEKLY CASCADE")
        weekly_cleanup()
    daily_cleanup()


def monthly_cleanup():
    """Move and delete backups to retain monthly backup archives."""
    s3_files = s3.read_files()

    weekly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    monthly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.MONTHLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if weekly[0][1] > monthly[0][1]:
        new_fpath = weekly[0][0].replace(
            config.WEEKLY_PREFIX, config.MONTHLY_PREFIX, 1)
        s3.copy(
            weekly[0],
            new_fpath
        )
        monthly.insert((new_fpath, date.today()), 0)

    string_monthly_records = '\n'.join([
        f"{f} | {m.isoformat()}"
        for f, m in monthly
    ])
    logger.debug(f"Current monthly records:\n{string_monthly_records}")

    if len(monthly) > config.MONTHLY_RECORDS:
        oldest = monthly[config.MONTHLY_RECORDS:]
        for f in oldest:
            s3.remove(f)


def weekly_cleanup():
    """Move and delete backups to retain weekly backup archives."""
    s3_files = s3.read_files()

    daily = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    weekly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if daily[0][1] > weekly[0][1]:
        new_fpath = daily[0][0].replace(
            config.DAILY_PREFIX, config.WEEKLY_PREFIX, 1)
        s3.copy(
            daily[0][0],
            new_fpath
        )
        weekly.insert(new_fpath, 0)

    string_weekly_records = '\n'.join([
        f"{f} | {m.isoformat()}"
        for f, m in weekly
    ])
    logger.debug(f"Current weekly records:\n{string_weekly_records}")

    if len(weekly) > config.WEEKLY_RECORDS:
        oldest = weekly[config.WEEKLY_RECORDS:]
        for f in oldest:
            s3.remove(f)


def daily_cleanup():
    """Move and delete backups to retain daily backup archives."""
    s3_files = s3.read_files()

    daily = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    string_daily_records = '\n'.join([
        f"{f} | {m.isoformat()}"
        for f, m in daily
    ])
    logger.debug(f"Current daily records:\n{string_daily_records}")

    if len(daily) > config.DAILY_RECORDS:
        oldest = daily[config.DAILY_RECORDS:]
        for f in oldest:
            s3.remove(f)
