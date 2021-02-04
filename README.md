# aws-backup

Automatic archiving of database and file system backups to AWS S3 storage

### A few assumptions:

- You have access to an AWS S3 bucket
- You are running this with `cron` on linux
- You have a `python 3.8` installation accessible to `/usr/bin/env`
- You have deployed a set of projects on a server which are writing to a PostgreSQL database cluster
- You have installed and configured `awscli` (see (here)[https://linuxhint.com/install_aws_cli_ubuntu/])
- There is suffient disk space in the repository to create a temporary DB dump

## PostgreSQL backup setup

We are assuming that there is a Postgresql cluster running that is accessible with the `pg_dumpall` command, which is used to create a DB dump of all databases on the cluster. You will also need to ensure that `awscli` is configured and accessible for the `postgres` user (or any Postgresql superuser), and that the `postgres` dir is writable by that user.

When run, the `postgres/pg_backup` will gzip the DB dump and send it to AWS S3 storage. It will copy existing backup files to create the specified weekly and monthly backups, before cleaning up old backup files.

- Git clone this repository to a location with plenty of disk space, that is writable by the `postgres` user
- Modify backup/config.py with your credentials and desired parameters
- Set up a `cron` job to run `pg_backup` once daily (detailed in the header of `pg_backup`)
