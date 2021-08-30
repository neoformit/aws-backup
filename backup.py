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
"""

import os

from config import config
from backup import cascade
from backup.postgres import pgdump

os.chdir(config['WORKING_DIR'])
pgdump.to_s3()
cascade.make()
