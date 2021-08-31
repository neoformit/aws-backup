#!/usr/bin/env python3

"""Backup files to AWS, keeping daily, weekly and monthly records."""

from config import config

from . import dispatch
from .project import ProjectBackup


def files():
    """Backup filesystem to S3."""
    pb = ProjectBackup(
        config.FILESYSTEM_PROJECT_ROOT,
        lof_file=config.FILESYSTEM_BACKUP_PATHS_LOG,
    )
    pb.build_archives()
    pb.dispatch_to_s3()
