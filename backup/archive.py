#!/usr/bin/env python3.8

"""Make backups of Postgresql cluster and filesystems.

Dispatch to AWS S3.
"""

import logging
from datetime import date

from config import config
from . import postgres
from .notifications import send_mail
from .filesystem.project import ProjectBackup

logger = logging.getLogger(__name__)


def pgdump():
    """Run backup cascade."""
    today = date.today()

    try:
        if today.day == config.MONTHLY_BACKUP_DAY:
            logger.info(80 * '-')
            logger.info(f"Month day {today.day}: PERFORMING MONTHLY CASCADE")
            logger.info(80 * '-')
            postgres.monthly.make()

        if today.weekday() == config.WEEKLY_BACKUP_WEEKDAY:
            logger.info(80 * '-')
            logger.info(
                f"Week day {today.weekday()}: PERFORMING WEEKLY CASCADE")
            logger.info(80 * '-')
            postgres.weekly.make()

        logger.info(80 * '-')
        logger.info('CASCADING DAILY BACKUPS')
        logger.info(80 * '-')
        postgres.daily.make()

    except Exception as exc:
        send_mail('Error encountered making DB cascade:', error=True)
        raise exc


def files():
    """Backup filesystem to S3."""
    try:
        pb = ProjectBackup(
            config.FILESYSTEM_PROJECT_ROOT,
            log_file=config.FILESYSTEM_BACKUP_PATHS_LOG,
        )
        pb.build_archives()
        pb.dispatch_to_s3()
    except Exception as exc:
        send_mail('Error encountered making project backups:', error=True)
        raise exc
