#!/usr/bin/env python3.8

"""Make backups of all DBs Postgresql cluster and dispatch to AWS S3."""

from backup import daily, weekly, monthly

monthly.make()
weekly.make()
daily.make()
