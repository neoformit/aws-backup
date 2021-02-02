#!/usr/bin/env bash

export HOME=/var/lib/postgresql
export PATH=$PATH:/usr/local/bin

cd /mnt/vdisk/postgresql/backup/monthly
echo `./monthly_backup.py`
