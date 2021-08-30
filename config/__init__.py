"""Read in configuration."""

import yaml
import logging
from logging.config import dictConfig


# Read in YAML configuration
# ------------------------------------------------------------------------------
if not os.path.exists('config.yml'):
    raise FileNotFoundError(
        "Please create 'config.yml' from the sample template provided.")

with open('config.yml') as f:
    config = yaml.safe_load(f)


# Check configuration
# ------------------------------------------------------------------------------

required_paths = (
    config['USER_HOME'],
    config['LOG_FILE_PATH'],
)

required_commands = (
    config['AWS_CMD'],
)

for p in required_paths:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Config path could not be found: {p}")

for c in required_commands:
    result = subprocess.call(['which', c], check=True)
    if not result.stdout:
        raise RuntimeError(f"No such command: {c}")


# Logging configuration
# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': config['LOG_FILE_PATH'] or 'backup.log',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
})
