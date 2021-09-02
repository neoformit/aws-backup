"""Command line arguments to be fed to argparse."""

ARGS = {
    '--dry': {
        'dest': 'DRY_RUN',
        'action': 'store_true',
        'default': False,
        'help': "Show intentions but don't do anything",
    },
    '--initial': {
        'dest': 'INITIAL',
        'action': 'store_true',
        'default': False,
        'help': "Ignore timestamps and back up filesystems for all projects",
    },
    '--verbose': {
        'dest': 'DEBUG',
        'action': 'store_true',
        'default': False,
        'help': "Verbose log output for debugging",
    },
}
