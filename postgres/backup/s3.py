"""Functions for interacting with AWS S3 storage."""

import os
import subprocess
from datetime import datetime

from .config import S3_PATH


def read(contains=None):
    """Read files listed under S3 bucket path and return stdout."""
    args = [
        'aws',
        's3',
        'ls',
        S3_PATH,
    ]
    files = {}
    result = subprocess.run(args, stdout=subprocess.PIPE, check=True)
    file_lines = result.stdout.decode('utf-8').split('\n')

    for line in file_lines:
        if not line:
            continue
        cols = [x for x in line.split(' ') if x]
        timestamp = datetime.strptime(' '.join(cols[:2]), '%Y-%m-%d %H:%M:%S')
        filename = cols[-1]
        files[filename] = timestamp

    if contains:
        return {
            k: v for k, v in files.items()
            if contains in k
        }
    return files


def copy(source, dest):
    """Copy file in S3 storage."""
    args = [
        'aws',
        's3',
        'cp',
        source,
        dest,
    ]
    subprocess.run(args, check=True)


def remove(path):
    """Remove specified filename from S3 storage under S3_PATH."""
    args = [
        'aws',
        's3',
        'rm',
        os.path.join(S3_PATH, path),
    ]
    subprocess.run(args, check=True)
