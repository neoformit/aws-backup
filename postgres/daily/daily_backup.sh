#!/usr/bin/env bash

export HOME=/var/lib/postgresql
export PATH=$PATH:/usr/local/bin

cd /mnt/vdisk/postgresql/backup/daily
./pg_backup.sh
echo `./daily_backup.py`
