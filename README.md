# aws-backup

Automatic archiving of database and file system backups to AWS S3 storage,
with cascading daily, weekly and monthly backups.

## A few assumptions:
- You have access to an AWS S3 bucket
- You schedule this program to run with `cron` on linux
- You have `python>=3.6` accessible to `/usr/bin/env`
- You have installed `virtualenv` to create a virtual environment
- You have deployed a set of projects on the host machine which are writing to a PostgreSQL database cluster
- These projects may also have files that you wish to be backed up (e.g. media files, data uploads)
- There is suffient disk space in the working directory to create temporary DB dumps and filesystem tarballs


## Setup

```sh
git clone https://github.com/neoformit/aws-backup.git
virtualenv --python=`which python3` venv
source venv/bin/activate
pip install -r requirements.txt
```

- Configure `awscli` with your user credentials ((instructions here)[https://linuxhint.com/install_aws_cli_ubuntu/])
- Copy `config.yml.sample` to `config.yml` and modify to suit your requirements
- Run `crontab -e` and add the following line, replacing PWD with the repository path:
    `3 0 * * *    source <PWD>/venv/bin/activate && <PWD>/run.py`


## How it works

**Database**

We are assuming that there is a Postgresql cluster running that is accessible with the `pg_dumpall` command, which is used to create a DB dump of all databases on the cluster. We also assume that the use running this program has `sudo` access to enable calling of `pg_dumpall` as the `postgres` user.

When run, `pg_backup` will gzip the DB dump and send it to AWS S3 storage. It will then copy existing S3 archives to create the specified weekly and monthly backups, before cleaning up old backup archives.

**Filesystem**

- Files to be backed up must be readable to the user running the program

The config variable `FILESYSTEM_PROJECT_ROOT` can be set to determine which folders will be scanned for file backups. All subfolders of this directory will be considered as a "project". In order for files to be backed up within a project, the project root must contain the file `backup.paths`, which specifies which file paths should be backed up for that project using `.gitignore` syntax. If a project does not contain a `backup.paths` file, no backups will be made. To back up an entire project, simply create a `backup.paths` containing `*`.
