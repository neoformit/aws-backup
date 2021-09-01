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
        if today.day == config['MONTHLY_BACKUP_DAY']:
            logger.debug('Cascading monthly backups...\n')
            postgres.monthly.make()

        if today.weekday() == config['WEEKLY_BACKUP_WEEKDAY']:
            logger.debug('Cascading weekly backups...\n')
            postgres.weekly.make()

        logger.debug('Cascading daily backups...\n')
        postgres.daily.make()

    except Exception as exc:
        send_mail(f'The following error was encountered:\n\n{exc}')


def files():
    """Backup filesystem to S3."""
    pb = ProjectBackup(
        config.FILESYSTEM_PROJECT_ROOT,
        log_file=config.FILESYSTEM_BACKUP_PATHS_LOG,
    )
    pb.build_archives()
    pb.dispatch_to_s3()
