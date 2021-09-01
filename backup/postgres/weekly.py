#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N weeks."""

import os
import logging
from operator import itemgetter
from datetime import datetime, timedelta

from . import s3
from config import config

logger = logging.getLogger(__name__)


def make():
    """Make weekly backup from daily backup file and remove old files."""
    create_weekly_from_daily()
    files = s3.read(contains=config.WEEKLY_PREFIX)
    n_weeks_ago = datetime.now() - timedelta(weeks=config.WEEKS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_weeks_ago
    }
    if old_files:
        logger.debug(
            "Removing old files from S3 storage:\n"
            + ' '.join(old_files.keys())
            + "\n"
        )
        for fname in old_files:
            s3.remove(fname)
        logger.debug("Done")
    else:
        logger.debug("No old files to remove")


def create_weekly_from_daily():
    """Copy lastest daily backup to convert to weekly backup."""
    daily_files = s3.read(contains=config.DAILY_PREFIX)
    if not daily_files:
        logger.debug("Can't make weekly backup, no daily backups yet.")
        return
    files_by_date = sorted(
        list(daily_files.items()),
        key=itemgetter(1),
    )
    oldest = files_by_date[0][0]
    new_fname = oldest.replace(config.DAILY_PREFIX, config.WEEKLY_PREFIX)
    logger.debug(
        f"Creating weekly backup file {new_fname} from daily file {oldest}")
    s3.copy(
        os.path.join(config.S3_POSTGRES_PATH, oldest),
        os.path.join(config.S3_POSTGRES_PATH, new_fname),
    )
