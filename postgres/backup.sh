#!/usr/bin/env bash

export HOME=/var/lib/postgresql
export PATH=$PATH:/usr/local/bin

cd /home/dev/backup
./backup.py
