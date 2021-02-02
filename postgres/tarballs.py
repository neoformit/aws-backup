"""Back up specified paths from projects under BASE_DIR as tar archives."""

import os
import tarfile
from time import time
from datetime import date
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


class ProjectBackup:
    """Back up specified project files as tar archives.

    All dirs under base_dir (first arg) are considered as project dirs.

    Specify files to back up in each project dir by adding the file
    "backup.paths" (.gitignore syntax) to a project's root dir.

    Set intial=True to force back up of all project's backup.paths.

    Add file flag backup.initial to project dir to force back up of specific
    project's backup.paths.

    If no backup.paths file is present in project dir, nothing will be backed
    up.

    Add a backup.paths file with the line '*' to back up everything.
    """

    def __init__(self, base_dir, initial=False):
        """Create project backup and collect archive file names."""
        self.today = date.today().strftime('%Y-%m-%d')
        self.BASE_DIR = base_dir
        self.INITIAL = initial
        if initial:
            print("Initial backup: backing up all projects...")
        self.project_paths = [
            x for x in os.listdir(self.BASE_DIR)
            if os.path.isdir(os.path.join(self.BASE_DIR, x))
        ]
        self.archives = self.make_tarballs()

    def make_tarballs(self):
        """Create tarballs for all dirs in base_dir.

        Only files listed under a project's backup.paths file will be included.

        Returns a list of relative paths for tar archives created.
        """
        archives = []

        for dpath in self.project_paths:
            try:
                fpaths = self.get_backup_filepaths(dpath)
                if fpaths is None:
                    print(
                        f"\nProject {dpath}:",
                        "no backup.paths file. Skipping..."
                    )
                    continue

                print(f"\nProject: {dpath}")
                print("-" * 80)

                if not (self.INITIAL or self.is_initial_project_backup(dpath)):
                    if not self.files_modified(fpaths):
                        print(
                            f"\nProject {dpath}:",
                            "no files modified. Skipping..."
                        )
                        continue

                print("Making backup...")
                tarname = self.compress_files(dpath, fpaths)
                archives.append(tarname)
                print(f"Tarball created: {tarname}")

            except Exception as exc:
                # Email error message and continue
                # But raise while in dev
                raise exc

        return archives

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
            print(f"Project {dpath} flagged as initial")
            return True
        return False

    def files_modified(self, fpaths):
        """Return True if files have been modified in last 25 hrs."""
        one_day_ago = time() - 90000  # 25 hours ago
        for f in fpaths:
            if os.path.getmtime(os.path.join(self.BASE_DIR, f)) > one_day_ago:
                print(f"File modified in past 25hrs: {f}")
                return True
        return False

    def compress_files(self, dpath, fpaths):
        """Compress files into a tar.gz archive."""
        tarname = f'daily_{self.today}_{dpath}.tar.gz'
        try:
            with tarfile.open(tarname, 'w:gz') as tar:
                for f in fpaths:
                    fpath = os.path.join(self.BASE_DIR, f)
                    print(f"Adding {fpath} to archive...")
                    tar.add(fpath)
        except Exception as exc:
            os.remove(tarname)
            raise exc
        return tarname


if __name__ == '__main__':
    backup = ProjectBackup('code')
    print(f"\nBackups created: {backup.archives}")
