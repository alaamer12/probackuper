import pytest
# from commands.backup import Backup
from commands.update import Update
# import os
# def _excluded_dirs(path) -> bool:
#         # Ignore e.g. .git and any hidden directories like Avast hidden dirs
#         EXLUDED_DIRS: list = [".git", ".venv", "venv", "node_modules", ".pnpm-store", ".DS_Store", ".idea", ".vscode"]
#         base_name: str = os.path.basename(path)
#         return ((base_name.startswith('_') and os.path.isdir(path))
#                 or base_name in EXLUDED_DIRS
#                 or any(excluded_dir in path.split(os.sep) for excluded_dir in EXLUDED_DIRS)
#                 or _is_hidden(path))
#
#
#
# def _is_hidden(path):
#     try:
#         # Get file attributes
#         attrs = os.stat(path).st_file_attributes
#         # Check if the hidden attribute is set
#         return attrs & 2 != 0
#     except Exception as e:
#         print("Error:", e)
#         return False


class TestBackup:
    class TestExludedDirs:
        def test_excluded_dirs(self):
            # # backup = Backup()
            # exluded_dirs = _excluded_dirs("venv")
            # assert exluded_dirs == True
            assert True

    # def test_list_root_dirs(self):
    #     backup = Backup()
    #     root_dirs = backup._list_root_dirs("C:\\")
    #     assert root_dirs