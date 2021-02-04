"""Make backups of all DBs Postgresql cluster and dispatch to AWS S3."""

import daily
import weekly
import monthly

monthly.make()
weekly.make()
daily.make()
