# To do

- [x] Update all import statements and config references
  - [x] Backup/filesystem
  - [x] Backup/postgres
- [x] Get logger working
- [x] Enable filesystem backups
- [x] Swap print for log statements
- [x] Fix filesystem logic to cascade across projects
- [x] Add run script callable from cron
- [ ] SQL dump per-database (per-table?)
- [ ] Store SQL archive hashes to avoid dispatch of duplicates
- [ ] Catch project archive error, email notification and continue
- [ ] Testing with time-machine https://pypi.org/project/time-machine/
- [ ] Catch and handle permission errors reading FS paths?
