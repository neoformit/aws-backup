"""General utilities."""

import os

TEMP_DIRNAME = 'tmp'


def tmp(filepath):
    """Create temp file dir if not exists."""
    if not os.path.exists(TEMP_DIRNAME):
        os.mkdir(TEMP_DIRNAME)
    return os.path.join(TEMP_DIRNAME, filepath)
