"""Back up specified paths from projects under BASE_DIR as tar archives."""

import os
import json
import tarfile
import logging
from time import time
from datetime import date
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from config import config
from backup.utils import tmp
from . import dispatch, s3

logger = logging.getLogger(__name__)


class ProjectBackup:
    """Back up specified project files as tar archives.

    All direct child dirs of base_dir (first arg) are considered as projects.

    Specify files to back up in each project dir by adding the file
    `backup.paths` (.gitignore syntax) to a project's root dir. If
    `backup.paths` does not exist, no file backups will be made.

    By default, a project backup will only run when files have been modified in
    the last 25 hours. This prevents duplicate backups from being made for a
    project when content is unchanged.

    Add file flag `backup.initial` to project dir to force back up of specific
    project's `backup.paths` (i.e. new project created). Add `backup.initial`
    to the project root dir to flag all projects as inital backups
    (i.e. first ever run). Note that there is nothing 'dangerous' about running
    initial, it just saves some time and disk space in the long-run on dormant
    applications.

    Add a `backup.paths` file with the line '*' to back up everything.
    """

    def __init__(self, base_dir, log_file=None):
        """Create project backup and collect archive file names."""
        self.BASE_DIR = base_dir
        self.INITIAL = self.is_initial_global_backup()
        self.log_file = log_file
        self.paths_record_file = tmp('project_paths.json')
        self.archived_project_paths = self.get_archived_paths()
        self.today = date.today().strftime('%Y-%m-%d')

        self.project_dirs = [
            x for x in os.listdir(self.BASE_DIR)
            if os.path.isdir(os.path.join(self.BASE_DIR, x))
        ]

        if self.log_file:
            with open(self.log_file, 'w') as f:
                f.write(f'# Written {self.today}\n\n')
                f.write('# Projects backed up to S3 in this run:\n')
                f.write('\n'.join(self.project_dirs) + '\n')

    def build_archives(self):
        """Create tarballs for all dirs in base_dir.

        Only files listed under a project's backup.paths file will be included.

        Returns a list of relative paths for tar archives created.
        """
        archives = []
        project_filepaths = {}

        for dpath in self.project_dirs:
            try:
                fpaths = self.get_backup_filepaths(dpath)
                if fpaths is None:
                    logger.debug(
                        f"\nProject {dpath}:"
                        " no backup.paths file. Skipping..."
                    )
                    continue

                project_filepaths[dpath] = fpaths

                if self.log_file:
                    with open(self.log_file, 'a') as f:
                        f.write(
                            f"\n# Archived files for project '{dpath}':\n"
                            + '\n'.join(sorted(fpaths))
                            + '\n'
                        )

                logger.debug("-" * 80)
                logger.debug(f"Project: {dpath}")

                if not (self.INITIAL or self.is_initial_project_backup(dpath)):
                    if not self.files_modified(dpath, fpaths):
                        logger.info(
                            f"Skipping project {dpath}: no files modified")
                        continue

                logger.debug("Making backup...")
                tarname = self.tar(dpath, fpaths)
                archives.append(tarname)
                logger.debug(f"Tarball created: {tarname}")

            except Exception as exc:
                # (not yet configured)
                # Email error message and continue
                # But raise while in dev
                # if config.DEBUG:
                #     raise exc
                raise exc

        with open(self.paths_record_file, 'w') as f:
            json.dump(project_filepaths, f)

        self.archives = archives

    def dispatch_to_s3(self):
        """Dispatch archives to S3 and clean up."""
        s3.store(
            self.archives,
            config.S3_FILES_PATH,
        )
        dispatch.cascade(self.project_dirs)

    def get_archived_paths(self):
        """Return dict of filepaths backed up on last run."""
        if os.path.exists(self.paths_record_file):
            with open(self.paths_record_file) as f:
                return json.load(f)

    def get_backup_filepaths(self, dpath):
        """Return filtered list of file paths."""
        fname = os.path.join(self.BASE_DIR, dpath, 'backup.paths')
        if not os.path.exists(fname):
            return
        backup_spec = open(fname).read()
        spec = PathSpec.from_lines(
            GitWildMatchPattern,
            backup_spec.splitlines()
        )
        return [
            os.path.join(dpath, p)
            for p in spec.match_tree(os.path.join(self.BASE_DIR, dpath))
        ]

    def is_initial_project_backup(self, dpath):
        """Return true if project flagged as inital backup."""
        flag = os.path.join(self.BASE_DIR, dpath, 'backup.initial')
        if os.path.exists(flag):
            os.remove(flag)
            logger.debug(f"Project {dpath} flagged as initial")
            return True
        return False

    def is_initial_global_backup(self):
        """Return true if projects root flagged as inital backup."""
        if config.INITIAL:
            logger.info("Flagged as initial backup - archiving all projects")
            return True
        flag = os.path.join(self.BASE_DIR, 'backup.initial')
        if os.path.exists(flag):
            os.remove(flag)
            logger.info(
                "Project root flagged as initial - setting INITIAL=True")
            return True
        return False

    def files_modified(self, dpath, fpaths):
        """Check if files have been modified or created in last 25hrs."""
        one_day_ago = time() - 90000  # 25 hours ago

        # Check if files created
        if (not self.archived_project_paths or
                dpath not in self.archived_project_paths):
            # No record of backed-paths - assume that all filepaths are new
            return True
        new_files = set(fpaths) - set(self.archived_project_paths[dpath])
        if new_files:
            msg = "File(s) created since last run:/n%s" % '\n'.join(new_files)
            logger.debug(msg)
            return True

        # Check if files modified
        for f in fpaths:
            if os.path.getmtime(os.path.join(self.BASE_DIR, f)) > one_day_ago:
                logger.debug(f"File modified in past 25hrs: {f}")
                return True
        return False

    def tar(self, dpath, fpaths):
        """Compress files into a tar.gz archive."""
        tarname = tmp(f'daily_{self.today}_{dpath}.tar.gz')
        try:
            with tarfile.open(tarname, 'w:gz') as tar:
                for f in fpaths:
                    fpath = os.path.join(self.BASE_DIR, f)
                    logger.debug(f"Adding <PROJECT_ROOT>/{f} to archive...")
                    tar.add(fpath)
        except Exception as exc:
            os.remove(tarname)
            raise exc
        return tarname


if __name__ == '__main__':
    backup = ProjectBackup('code')
    print(f"\nBackup created: {backup.archives}")
