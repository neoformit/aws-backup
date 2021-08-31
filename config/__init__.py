"""Read in configuration."""

import os
import yaml
import logging
import logging.config
import subprocess
from types import SimpleNamespace

# Read in YAML configuration
# ------------------------------------------------------------------------------
if not os.path.exists('config.yml'):
    raise FileNotFoundError(
        "Please create 'config.yml' from the sample template provided.")

with open('config.yml') as f:
    config = SimpleNamespace(**yaml.safe_load(f))


# Check configuration
# ------------------------------------------------------------------------------

required_paths = (
    config.USER_HOME,
    config.WORKING_DIR,
    config.LOG_FILE_PATH or config.WORKING_DIR,
)

required_commands = (
    config.AWS_CMD,
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
logger = logging.getLogger(__name__)
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
            'filename': config.LOG_FILE_PATH or 'backup.log',
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
