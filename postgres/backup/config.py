"""Postgres backup configuration."""

# AWS S3 path for backup location
S3_PATH = 's3://neoform-backup/postgresql/'

# Number of backups at each level
DAYS = 7
WEEKS = 4
MONTHS = 6

# Day of week for weekly backup (0-6 : Mon-Sun)
WEEKLY_BACKUP_WEEKDAY = 5

# Day of month for monthly backup ( =< 28)
MONTHLY_BACKUP_DAY = 1

# Prefixes to identify backup files by level
DAILY_PREFIX = 'daily'
WEEKLY_PREFIX = 'weekly'
MONTHLY_PREFIX = 'monthly'
