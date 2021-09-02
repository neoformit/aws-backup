"""Initialize backup."""

from config import config

from .postgres import pgdump
from . import archive


def make():
    """Backup postgres cluster and project filesystems to AWS S3."""
    pgdump.to_s3()
    archive.pgdump()
    archive.files()
