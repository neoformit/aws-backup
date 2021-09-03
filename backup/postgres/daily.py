#!/usr/bin/env python3.8

"""Remove files from S3 storage older than N days."""

import logging
from datetime import datetime, timedelta

from . import s3
from config import config

logger = logging.getLogger(__name__)


def make():
    """Clean up old daily backup files."""
    files = s3.read(contains=config.DAILY_PREFIX)
    logger.debug("Daily backup files currently in S3 storage:")
    for k, v in files.items():
        logger.debug(f'{k.ljust(30)} | {v.strftime("%Y-%m-%d %H:%M:%S")}')

    n_days_ago = datetime.now() - timedelta(days=config.DAYS)
    old_files = {
        k: v for k, v in files.items()
        if v < n_days_ago
    }

    if old_files:
        logger.info(f"Removing {len(old_files)} old archives:")
        for fname in old_files:
            logger.info(f"\t{fname}")
            s3.remove(fname)
    else:
        logger.debug("No old files to remove")
