"""AWS S3 file operations."""

import os
import logging
import subprocess
from datetime import datetime

from config import config

logger = logging.getLogger(__name__)


def read_files(contains=None):
    """Read files listed under given S3 bucket path.

    Return a dict of {filename<string>: timestamp<datetime.datetime>}
    """
    args = [
        config.AWS_CMD,
        's3',
        'ls',
        config.S3_FILES_PATH,
    ]
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE)
    s3_files = result.stdout.decode('utf-8').split('\n')

    files = {}
    for line in s3_files:
        cols = [x for x in line.split(' ') if x]
        timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
        filename = cols[-1]
        files[filename] = timestamp

    if contains:
        files = {
            k: v
            for k, v in files.items()
            if k.contains(contains)
        }

    string_files = '\n'.join([
        f"{f} | {m.isoformat()}"
        for f, m in files.items()
    ])
    logger.debug(f"List filesystem archives in S3:\n{string_files}")
    return files


def store(filepaths, dest):
    """Send all files in filepaths[] to S3 storage under dest dir."""
    logger.debug(f"Dispatching {len(filepaths)} files to S3...")
    for f in filepaths:
        d = os.path.join(dest, os.basename(f))
        move(f, d)


def copy(src, dest):
    """Copy s3 file to new location."""
    args = [
        config.AWS_CMD,
        's3',
        'cp',
        os.path.join(config.S3_FILES_PATH, src),
        os.path.join(config.S3_FILES_PATH, dest)
    ]
    logger.debug(f"RUN: {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True)


def move(src, dest):
    """Move s3 file to new location."""
    args = [
        config.AWS_CMD,
        's3',
        'mv',
        os.path.join(config.S3_FILES_PATH, src),
        os.path.join(config.S3_FILES_PATH, dest)
    ]
    logger.debug(f"RUN: {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True)


def remove(path):
    """Remove s3 file."""
    args = [
        config.AWS_CMD,
        's3',
        'rm',
        os.path.join(config.S3_FILES_PATH, path)
    ]
    logger.debug(f"RUN: {' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True)
