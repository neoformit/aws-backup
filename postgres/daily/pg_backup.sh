#!/usr/bin/env bash

cd /mnt/vdisk/postgresql/backup

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
