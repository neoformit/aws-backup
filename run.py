#!/usr/bin/env python3

"""Run backups for the day.

Schedule can be configured with config.yml

- Create a database dump from the local postgres cluster using pg_dumpall
- Make filesystem backups as specified in `backup.paths` records per-project
- Send the compressed dump archives to configured AWS S3 storage locations
- Rename and delete objects on AWS to maintain daily, weekly and monthly
  backups as per configuration (AKA "cascade").

Execution of this file should be scheduled to run with Cron or similar at the
same time every day.

Set run parameters in `config.yml` e.g. day-of-month to take monthly backup.
"""

import os
import logging
from argparse import ArgumentParser

import backup
from config import config
from config.args import ARGS

logger = logging.getLogger(__name__)


def main():
    """Run backups."""
    os.chdir(config.WORKING_DIR)
    backup.make()


def set_args():
    """Parse command line arguments."""
    ap = ArgumentParser(
        description='Back up project databases and filesystems.')
    for name, params in ARGS.items():
        ap.add_argument(name, **params)
    args = ap.parse_args()
    config.update(vars(args))


if __name__ == '__main__':
    print("Loaded modules")
    set_args()
    main()
