"""AWS S3 file operations."""

import os
import subprocess
from datetime import datetime

S3_PATH = 's3://neoform-backup/files/'


def read_files():
    """Read files listed under given S3 bucket path and return stdout."""
    args = [
        'aws',
        's3',
        'ls',
        S3_PATH,
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


def store(filepaths):
    """Send all tar archives in base_dir to S3 storage."""
    for f in filepaths:
        args = [
            'aws',
            's3',
            'mv',
            f,
            os.path.join(S3_PATH, f),
        ]
        subprocess.run(args, check=True)


def copy(src, dest):
    """Move s3 file to new location."""
    args = [
        'aws',
        's3',
        'cp',
        os.path.join(S3_PATH, src),
        os.path.join(S3_PATH, dest)
    ]
    subprocess.run(args, check=True)


def move(src, dest):
    """Move s3 file to new location."""
    args = [
        'aws',
        's3',
        'mv',
        os.path.join(S3_PATH, src),
        os.path.join(S3_PATH, dest)
    ]
    subprocess.run(args, check=True)


def remove(path):
    """Move s3 file to new location."""
    args = [
        'aws',
        's3',
        'rm',
        os.path.join(S3_PATH, path)
    ]
    subprocess.run(args, check=True)
