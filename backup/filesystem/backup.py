#!/usr/bin/env python3

"""Backup files to AWS, keeping daily, weekly and monthly records."""

from . import dispatch
from .tarballs import ProjectBackup

BASE_DIR = '/home/dev/code/'
backup = ProjectBackup(BASE_DIR, initial=True)
dispatch.to_s3_storage(backup.archives)
dispatch.cleanup()
