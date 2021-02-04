#!/usr/bin/env python3.8

"""Make backups of all DBs Postgresql cluster and dispatch to AWS S3."""

from datetime import date
from backup import daily, weekly, monthly
from backup.config import WEEKLY_BACKUP_WEEKDAY, MONTHLY_BACKUP_DAY

today = date.today()

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
