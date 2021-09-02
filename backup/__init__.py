"""Initialize backup."""

import math
import logging

from .postgres import pgdump
from . import archive

logger = logging.getLogger(__name__)


def make():
    """Backup postgres cluster and project filesystems to AWS S3."""
    logger.info(log_section("MAKE DATABASE DUMP"))
    pgdump.to_s3()
    logger.info(log_section("ARCHIVE DATABASES"))
    archive.pgdump()
    logger.info(log_section("ARCHIVE FILESYSTEMS"))
    archive.files()


def log_section(message):
    """Return message as log section header."""
    banner_length = math.floor((78 - len(message)) / 2)
    return (
        f"\n{ 80 * '=' }\n"
        f"{ banner_length * '~' } {message} { banner_length * '~' }\n"
        f"{ 80 * '=' }\n"
    )
