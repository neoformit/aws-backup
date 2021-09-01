#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N months."""

import os
import logging
from operator import itemgetter
from datetime import datetime, timedelta

from . import s3
from config import config

logger = logging.getLogger(__name__)


def make():
    """Make monthly backup from weekly backup files and remove old files."""
    files = s3.read(contains=config.MONTHLY_PREFIX)
    logger.debug("Monthly backup files currently in S3 storage:")
    for k, v in files.items():
        logger.debug(f'{k.ljust(30)} | {v.strftime("%Y-%m-%d %H:%M:%S")}')
    if not files:
        logger.debug("None")

    create_monthly_from_weekly()

    n_months_ago = datetime.now() - timedelta(days=config.MONTHS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_months_ago
    }

    if old_files:
        logger.debug(
            "Removing old files from S3 storage:\n"
            + ' '.join(old_files.keys())
            + '\n'
        )
        for fname, timestamp in old_files.items():
            s3.remove(fname)
        logger.debug("Done")
    else:
        logger.debug("No old files to remove")


def create_monthly_from_weekly():
    """Copy lastest weekly backup to convert to monthly backup."""
    weekly_files = s3.read(contains=config.WEEKLY_PREFIX)
    if not weekly_files:
        logger.debug("Can't make monthly backup, no weekly backups yet.")
        return
    files_by_date = sorted(
        list(weekly_files.items()),
        key=itemgetter(1),
    )
    oldest = files_by_date[0][0]
    new_fname = oldest.replace(config.WEEKLY_PREFIX, config.MONTHLY_PREFIX)
    logger.debug(
        f'Creating monthly backup file {new_fname}'
        f' from weekly backup {oldest}')
    s3.copy(
        os.path.join(config.S3_POSTGRES_PATH, oldest),
        os.path.join(config.S3_POSTGRES_PATH, new_fname),
    )
