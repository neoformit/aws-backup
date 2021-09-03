#!/usr/bin/env python3.8

"""Make backups of Postgresql cluster and filesystems.

Dispatch to AWS S3.
"""

import logging
from datetime import date

from config import config
from .utils import log_section
from . import postgres
from .notifications import send_mail
from .filesystem.projects import ProjectBackup

logger = logging.getLogger(__name__)


def make():
    """Backup postgres cluster and project filesystems to AWS S3."""
    log_section("MAKE DATABASE DUMP", major=True)
    postgres.pgdump.to_s3()
    log_section("CASCADE DATABASE ARCHIVES", major=True)
    archive_database()
    log_section("ARCHIVE FILESYSTEM", major=True)
    archive_filesystem()


def archive_database():
    """Run backup cascade."""
    today = date.today()

    try:
        if today.day == config.MONTHLY_BACKUP_DAY:
            log_section(f"Month day {today.day}: PERFORMING MONTHLY CASCADE")
            postgres.monthly.make()

        if today.weekday() == config.WEEKLY_BACKUP_WEEKDAY:
            log_section(
                f"Week day {today.weekday()}: PERFORMING WEEKLY CASCADE")
            postgres.weekly.make()

        log_section('PERFORMING FINAL CLEANUP')
        postgres.daily.make()

    except Exception as exc:
        send_mail('Error encountered making DB cascade:', error=True)
        raise exc


def archive_filesystem():
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
