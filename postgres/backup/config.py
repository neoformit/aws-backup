"""Postgres backup configuration."""

# Path to backup location on S3 storage
S3_PATH = 's3://neoform-backup/postgresql/'

# Prefixes to identify backup files by level
DAILY_PREFIX = 'daily'
WEEKLY_PREFIX = 'weekly'
MONTHLY_PREFIX = 'monthly'

# Number of backups at each level
DAYS = 7
WEEKS = 4
MONTHS = 6
