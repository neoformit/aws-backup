#/usr/bin/env bash

echo "Running AWS-backup with Cron..."
cd `dirname $0`
. venv/bin/activate && ./run.py
