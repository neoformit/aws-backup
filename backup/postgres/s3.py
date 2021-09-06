"""Functions for interacting with AWS S3 storage."""

import os
import logging
import subprocess
from datetime import datetime

from config import config

logger = logging.getLogger(__name__)


def read(contains=None):
    """Read files listed under S3 bucket path.

    Return a dict of {filename<string>: timestamp<datetime.datetime>}
    """
    args = [
        config.AWS_CMD,
        's3',
        'ls',
        config.S3_POSTGRES_PATH,
    ]
    logger.debug(f"RUN:\n\t$ {' '.join(args)}")
    files = {}
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode > 1:
        raise RuntimeError(result.stderr)
    file_lines = [
        x
        for x in result.stdout.decode('utf-8').split('\n')
        if x.strip()
    ]
    logger.debug("S3 FILES:\n\t%s" % '\n\t'.join(file_lines))

    for line in file_lines:
        if not line:
            continue
        cols = [x for x in line.split(' ') if x]
        timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
        filename = cols[-1]
        files[filename] = timestamp

    if contains:
        files = {
            k: v for k, v in files.items()
            if contains in k
        }

    return files


def move(source, dest):
    """Copy file in S3 storage."""
    args = [
        config.AWS_CMD,
        's3',
        'mv',
        source,
        dest,
    ]
    logger.debug(f"RUN:\n\t$ {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def copy(source, dest):
    """Copy file in S3 storage."""
    args = [
        config.AWS_CMD,
        's3',
        'cp',
        source,
        dest,
    ]
    logger.debug(f"RUN:\n\t$ {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def remove(path):
    """Remove specified filename from S3 storage under S3_POSTGRES_PATH."""
    args = [
        config.AWS_CMD,
        's3',
        'rm',
        os.path.join(config.S3_POSTGRES_PATH, path),
    ]
    logger.debug(f"RUN:\n\t$ {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
