"""General utilities."""

import os
import math
import logging

logger = logging.getLogger(__name__)
TEMP_DIRNAME = 'tmp'


def tmp(filepath):
    """Create temp file dir if not exists."""
    if not os.path.exists(TEMP_DIRNAME):
        os.mkdir(TEMP_DIRNAME)
    return os.path.join(TEMP_DIRNAME, filepath)


def log_section(message, major=False):
    """Return message as log section header."""
    ch = "=" if major else '-'
    banner_length = math.floor((78 - len(message)) / 2)
    logger.info(f"{ 80 * ch }")
    logger.info(f"{ banner_length * '~' } {message} { banner_length * '~' }")
    logger.info(f"{ 80 * ch }")
