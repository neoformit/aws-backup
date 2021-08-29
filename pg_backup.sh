#!/usr/bin/env bash

# This file should be configured to run with crontab like so, with logging
# being echoed to the designated log file path:

# WDIR=/mnt/vdisk/postgresql/backup  # << The current directory
# 30 12 * * * $WDIR/pg_backup.sh > $WDIR/backup.log 2>&1

if [ -z $WDIR ]; then
	WDIR=$PWD
fi

export HOME=/var/lib/postgresql
export PATH=$PATH:/usr/local/bin

cd $WDIR
echo "Making today's postgresql backup..."

# SQL dump
now="$(date +'%Y-%m-%d')"
fname="daily_$now.sql.gz"
echo "fname: $fname"
pg_dumpall | gzip > $fname

# Move to AWS S3
echo "Moving backup file to AWS..."
aws s3 mv $fname s3://neoform-backup/postgresql/$fname
echo "Done"

echo ""
echo "========================================================================="
echo "Cascading backups..."
echo ""

# Cascade backups to daily, weekly and monthly
python cascade.py
