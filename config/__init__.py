"""Read in configuration."""

import os
import yaml
import logging
import logging.config
import subprocess
from types import SimpleNamespace

logger = logging.getLogger(__name__)


# Read in YAML configuration
# ------------------------------------------------------------------------------
if not os.path.exists('config.yml'):
    raise FileNotFoundError(
        "Please create 'config.yml' from the sample template provided.")

with open('config.yml') as f:
    config = SimpleNamespace(**yaml.safe_load(f))


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
    with open('/dev/null', 'wb', 0) as null:
        result = subprocess.run(['which', c], check=True, stdout=null)
    if result.returncode != 0:
        raise RuntimeError(f"No such command: {c}")


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
            'filename': os.path.join(config.LOG_FILE_DIR, 'aws-backup.log'),
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
logging.root.setLevel(logging.DEBUG)
