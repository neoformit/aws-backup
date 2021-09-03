"""Back up tar archives to AWS S3 and clean up old files.

THIS WILL NOT CURRENTLY WORK ACROSS MULTIPLE PROJECT DIRS - THEY WILL ALL BE
CASCADED AS ONE.
"""

import logging
from datetime import date
from operator import itemgetter

from config import config

from . import s3

logger = logging.getLogger(__name__)


def cascade(project_paths):
    """Perform backup cascading over all projects."""
    for p in project_paths:
        cascade_project(p)


def cascade_project(project):
    """Run all cleanup operations to organise s3 backup archives."""
    today = date.today()
    if today.day == config.MONTHLY_BACKUP_DAY:
        logger.info(80 * "-")
        logger.info(
            f"Month day {today.day}: PERFORMING MONTHLY CASCADE"
            f" - {project}")
        logger.info(80 * "-")
        monthly_cleanup(project)
    if today.weekday() == config.WEEKLY_BACKUP_WEEKDAY:
        logger.info(80 * "-")
        logger.info(
            f"Week day {today.weekday()}: PERFORMING WEEKLY CASCADE"
            f" - {project}")
        logger.info(80 * "-")
        weekly_cleanup(project)
    logger.info(80 * "-")
    logger.info(f"PERFORMING FINAL CLEANUP - {project}")
    logger.info(80 * "-")
    daily_cleanup(project)


def monthly_cleanup(project):
    """Move and delete backups to retain monthly backup archives."""
    s3_files = s3.read_files(contains=project)

    weekly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if not weekly:
        logger.debug("No weekly archives available to create monthly backup")
        return

    monthly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.MONTHLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if not monthly or weekly[0][1] > monthly[0][1]:
        new_fpath = weekly[0][0].replace(
            config.WEEKLY_PREFIX, config.MONTHLY_PREFIX, 1)
        s3.copy(
            weekly[0][0],
            new_fpath
        )
        monthly.insert(0, (new_fpath, date.today()))

    string_monthly_records = '\n\t'.join([
        f"{f} | {m.isoformat()}"
        for f, m in monthly
    ])
    logger.debug(f"Current monthly archives:\n\t{string_monthly_records}")

    if len(monthly) > config.MONTHS:
        oldest = monthly[config.MONTHS:]
        logger.info(f"Removing {len(oldest)} old archives:")
        for f, m in oldest:
            logger.info(f"\t{f}")
            s3.remove(f)


def weekly_cleanup(project):
    """Move and delete backups to retain weekly backup archives."""
    s3_files = s3.read_files(contains=project)

    daily = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if not daily:
        logger.debug("No daily archives available to create monthly backup")
        return

    weekly = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.WEEKLY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    if not weekly or daily[0][1] > weekly[0][1]:
        new_fpath = daily[0][0].replace(
            config.DAILY_PREFIX, config.WEEKLY_PREFIX, 1)
        s3.copy(
            daily[0][0],
            new_fpath
        )
        weekly.insert(0, (new_fpath, date.today()))

    string_weekly_records = '\n\t'.join([
        f"{f} | {m.isoformat()}"
        for f, m in weekly
    ])
    logger.debug(f"Current weekly archives:\n\t{string_weekly_records}")

    if len(weekly) > config.WEEKS:
        oldest = weekly[config.WEEKS:]
        logger.info(f"Removing {len(oldest)} old archives:")
        for f, m in oldest:
            logger.info(f"\t{f}")
            s3.remove(f)


def daily_cleanup(project):
    """Move and delete backups to retain daily backup archives."""
    s3_files = s3.read_files(contains=project)

    daily = sorted([
        (f, m) for f, m in s3_files.items()
        if f.startswith(config.DAILY_PREFIX)
    ], key=itemgetter(1), reverse=True)

    string_daily_records = '\n\t'.join([
        f"{f} | {m.isoformat()}"
        for f, m in daily
    ])
    logger.debug(f"Current daily archives:\n\t{string_daily_records}")

    if len(daily) > config.DAYS:
        oldest = daily[config.DAYS:]
        logger.info(f"Removing {len(oldest)} old archives:")
        for f in oldest:
            logger.info(f"\t{f}")
            s3.remove(f)
