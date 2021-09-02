#!/usr/bin/env python3

"""Run backups for the day.

Schedule can be configured with config.yml

- Create a database dump from the local postgres cluster using pg_dumpall
- Send the compressed dump file to configured AWS S3 storage
- Rename and delete objects on AWS to maintain daily, weekly and monthly
  backups as per configuration

Not yet configured:

- Filesystem dumps with above as tarballs
- Filesystem dumps target specific paths in gitignore syntax as defined by
  `backup.paths` records in projects' root under configured PROJECT_BASE_DIR
- Add file flag backup.initial to project dir to force back up of that
  project's backup.paths regardless of timestamp.
"""

import os
import logging
from argparse import ArgumentParser

import backup
from config import config

logger = logging.getLogger(__name__)


def main():
    """Run backups."""
    set_args()
    logger.info("Loaded modules")
    os.chdir(config.WORKING_DIR)
    backup.make()


def set_args():
    """Parse command line arguments."""
    ap = ArgumentParser(description='Process some integers.')
    ap.add_argument(
        '--dry',
        dest='dry_run',
        action='store_true',
        default=False,
        help="Show intentions but don't do anything",
    )
    args = ap.parse_args()

    if args.dry_run:
        config.DRY_RUN = True


if __name__ == '__main__':
    print("Loaded modules")
    main()
