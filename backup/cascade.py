#!/usr/bin/env python3.8

"""Make backups of all DBs Postgresql cluster and dispatch to AWS S3."""

from datetime import date

from config import config
from . import  postgres
# from . import filesystem
from .notifications import send_mail


def make():
    """Run backup cascade."""
    today = date.today()

    try:
        if today.day == config['MONTHLY_BACKUP_DAY']:
            print('Cascading monthly backups...\n')
            postgres.monthly.make()
            print()

        if today.weekday() == config['WEEKLY_BACKUP_WEEKDAY']:
            print('Cascading weekly backups...\n')
            postgres.weekly.make()
            print()

        print('Cascading daily backups...\n')
        postgres.daily.make()
        print()

    except Exception as exc:
        send_mail(f'The following error was encountered:\n\n{exc}')
