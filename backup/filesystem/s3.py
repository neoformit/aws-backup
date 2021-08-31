"""AWS S3 file operations."""

import os
import subprocess
from datetime import datetime

from config import config


def read_files():
    """Read files listed under given S3 bucket path and return stdout."""
    args = [
        config.AWS_CMD,
        's3',
        'ls',
        config.S3_PATH,
    ]
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE)
    s3_files = result.stdout.decode('utf-8').split('\n')

    files = []
    for line in s3_files:
        cols = [x for x in line.split(' ') if x]
        timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
        filename = cols[-1]
        files.append(filename, timestamp)

    return files


def store(filepaths, dest):
    """Send all files in filepaths[] to S3 storage under dest dir."""
    for f in filepaths:
        d = os.path.join(dest, os.basename(f))
        move(f, d)


def copy(src, dest):
    """Copy s3 file to new location."""
    args = [
        config.AWS_CMD,
        's3',
        'cp',
        os.path.join(config.S3_PATH, src),
        os.path.join(config.S3_PATH, dest)
    ]
    subprocess.run(args, check=True)


def move(src, dest):
    """Move s3 file to new location."""
    args = [
        config.AWS_CMD,
        's3',
        'mv',
        os.path.join(config.S3_PATH, src),
        os.path.join(config.S3_PATH, dest)
    ]
    subprocess.run(args, check=True)


def remove(path):
    """Remove s3 file."""
    args = [
        config.AWS_CMD,
        's3',
        'rm',
        os.path.join(config.S3_PATH, path)
    ]
    subprocess.run(args, check=True)
