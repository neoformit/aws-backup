# aws-backup

Automatic archiving of database and file system backups to AWS S3 storage

This package (set of scripts, really) is designed to be run as a scheduled task with cron on linux.

It assumes that you have access to an AWS S3 bucket, and that there is a Postgresql cluster running that is accessible with the `pg_dumpall` command, which is used to create a DB dump of all databases on the cluster.

When run, the software will gzip  the DB dump and send it to AWS S3 storage. It will copy existing backup files to create the specified weekly and monthly backups, before cleaning up old backup files.

## Setup

- Install and configure `awscli` (see (here)[https://linuxhint.com/install_aws_cli_ubuntu/])
- Git clone this repository to a suitable location
- Navigate to a directory with plenty of disk space, that is writable by the `postgres` user
- Make a soft-link to the repository with `ln -s /path/to/aws-backup backup`
- Modify backup/config.py with your credentials/environment
- Set up a `cron` job to run `pg_backup.sh` once a day (details in the header of `pg_backup.sh`)
