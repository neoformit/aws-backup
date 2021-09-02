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
    logger.debug(f"RUN:\n\t${' '.join(args)}")
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

    files = {}
    for line in file_lines:
        cols = [x for x in line.split(' ') if x]
        timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
        filename = cols[-1]
        files[filename] = timestamp

    if contains:
        files = {
            k: v
            for k, v in files.items()
            if contains in k
        }

    return files


def store(filepaths, dest):
    """Send all files in filepaths[] to S3 storage under dest dir."""
    if not filepaths:
        logger.debug("No FS archives to dispatch to S3")
        return

    logger.debug(f"Dispatching {len(filepaths)} files to S3...")
    for f in filepaths:
        d = os.path.join(dest, os.path.basename(f))
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
    logger.debug(f"RUN:\n\t${' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def move(src, dest):
    """Move files between local and S3."""
    args = [
        config.AWS_CMD,
        's3',
        'mv',
        src,
        dest,
    ]
    logger.debug(f"RUN:\n\t${' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def remove(path):
    """Remove s3 file."""
    args = [
        config.AWS_CMD,
        's3',
        'rm',
        os.path.join(config.S3_FILES_PATH, path)
    ]
    logger.debug(f"RUN:\n\t${' '.join(args)}")
    if config.DRY_RUN:
        return
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
