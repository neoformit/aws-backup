"""Read in configuration."""

import os
import yaml
import logging
import logging.config
import subprocess

logger = logging.getLogger(__name__)


class Config:
    """Read in, store and update config."""

    def __init__(self, fname):
        """Read in config from yaml."""
        with open(fname) as f:
            config = yaml.safe_load(f)
        for k, v in config.items():
            setattr(self, k, v)

    def update(self, new):
        """Update config from dict.

        Will only create new attributes, only update existing.
        """
        for k, v in new.items():
            if hasattr(self, k):
                setattr(self, k, v)


# Read in YAML configuration
# ------------------------------------------------------------------------------
if not os.path.exists('config.yml'):
    raise FileNotFoundError(
        "Please create 'config.yml' from the sample template provided.")

config = Config('config.yml')


# Check configuration
# ------------------------------------------------------------------------------

if not config.WORKING_DIR:
    config.WORKING_DIR = os.getcwd()

if not config.LOG_FILE_DIR:
    config.LOG_FILE_DIR = config.WORKING_DIR

required_paths = (
    config.WORKING_DIR,
    config.LOG_FILE_DIR,
)

required_commands = (
    config.AWS_CMD,
    config.DB_DUMP_CMD,
)

for p in required_paths:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Config path could not be found: {p}")

for c in required_commands:
    result = subprocess.run(
        ['which', c],
        stdout=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command not found: {c}")


# Logging configuration
# ------------------------------------------------------------------------------
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '{levelname} | {asctime} | {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'delay': True,
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1000000,  # 1MB ~ 20k rows
            'backupCount': 5,
            'filename': os.path.join(config.LOG_FILE_DIR, 'backup.log'),
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
})
log_level = logging.DEBUG if config.DEBUG else logging.INFO
logging.root.setLevel(log_level)
