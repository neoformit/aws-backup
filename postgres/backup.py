#!/usr/bin/env python3.8

"""Make backups of all DBs Postgresql cluster and dispatch to AWS S3."""

from datetime import date
from notifications import send_mail
from backup import daily, weekly, monthly
from backup.config import WEEKLY_BACKUP_WEEKDAY, MONTHLY_BACKUP_DAY

today = date.today()

try:
    if today.day == MONTHLY_BACKUP_DAY:
        print('Cascading monthly backups...\n')
        monthly.make()
        print()

    if today.weekday() == WEEKLY_BACKUP_WEEKDAY:
        print('Cascading weekly backups...\n')
        weekly.make()
        print()

    print('Cascading daily backups...\n')
    daily.make()
    print()

except Exception as exc:
    send_mail(
        ['Cameron Hyde <chyde@neoformit.com>'],
        'Neoform Server <server@neoformit.com>',
        'PG backup error',
        f'The following error was encountered running pg_backup:\n{exc}'
    )
