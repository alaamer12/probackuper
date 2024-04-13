from .base_command import ICommand
import psutil
import os
from enum import Enum
from typing import Optional, List, Any, Union, Tuple, List
import shutil
import datetime
import sys
import subprocess
import logging
import tqdm
import string
import random
import logging
from .constants import (EXLUDED_DIRS, DEFAULT_INCLUDED,
                        UNIT_MULTIPLIER, SAFE_SPACE, UNIT)

TOTAL_SIZE = 0

"""Only Windows supported for now"""


# TODO: add support for partial backup
# TODO: add datetime, logging, error handling

class Backup(ICommand):
    def __init__(self, __particular_partition=None, __include: Optional[List[str], str] = None,
                 __dis: str = ".") -> None:
        self.__partitions = []
        self.__particular_partition = __particular_partition
        self.__include = __include
        self.__system_partition = f"{os.environ['SystemDrive']}\\"
        self.__dis = __dis

    @staticmethod
    def _create_name() -> str:
        # return "$bkup".join(random.choices(string.ascii_uppercase + string.digits, k=10)[0:4])
        return "$bkup"

    # def _get_valid_parts(self) -> Optional[list[str], tuple[bool, str, any]]:
    #     if isinstance(self._handle_particular_partition(), list):
    #         return self._handle_particular_partition()

    def _handle_particular_partition(self) -> Optional[list[str], tuple[bool, str, any]]:
        all_partitions = [p.mountpoint for p in psutil.disk_partitions()
                          if p.fstype == "NTFS" if p.mountpoint != self.__system_partition]
        # Return all __partitions if no particular partition is provided
        if self.__particular_partition is None:
            return all_partitions
        # Check if particular partition is mounted
        if not isinstance(self.__particular_partition, str):
            return False, self.__particular_partition, "Partition should be a string"

        # Getting all the __partitions and return True if particular partition is mounted
        try:
            if self.__particular_partition.upper() not in all_partitions:
                return False, self.__particular_partition, "Partition is not mounted"
            return True, self.__particular_partition, "Partition is mounted"
        except ValueError as e:
            return False, self.__particular_partition, e
        except Exception as e:
            print(e)
            return False, self.__particular_partition, e

    @staticmethod
    def _hide_directory(path) -> None:
        try:
            # Set the hidden attribute
            os.system('attrib +h "{}"'.format(path))
            print("Directory '{}' is now hidden.".format(path))
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def _unhide_directory(path):
        try:
            # Remove the hidden attribute
            os.system('attrib -h "{}"'.format(path))
            print("Directory '{}' is now visible.".format(path))
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def _is_hidden(path):
        try:
            # Get file attributes
            attrs = os.stat(path).st_file_attributes
            # Check if the hidden attribute is set
            return attrs & 2 != 0
        except Exception as e:
            print("Error:", e)
            return False

    @staticmethod
    def _list_included_dirs(_included_dirs) -> None:
        os.makedirs("logs", exist_ok=True)
        with open("logs/excluded_dirs.txt", "w") as f:
            for dir in _included_dirs:
                f.write(f"{dir}\n")

    @staticmethod
    def _list_included_files(_included_files) -> None:
        os.makedirs("logs", exist_ok=True)

        with open("logs/excluded_files.txt", "w") as f:
            for file in _included_files:
                f.write(f"{file}\n")

    def _exclude_dirs(self, path) -> bool:
        # Ignore e.g. .git and any hidden directories like Avast hidden dirs
        base_name: str = os.path.basename(path)

        return ((base_name.startswith('_') and os.path.isdir(path))
                or any(excluded_dir in path.split(os.sep) for excluded_dir in EXLUDED_DIRS)
                or self._is_hidden(path))

    # TODO: FIXIT
    # @staticmethod
    def _total_dir_size(self, src: str, unit: str = "GB") -> float:
        if unit not in UNIT_MULTIPLIER:
            raise ValueError(f"Invalid unit: {unit}")
        global TOTAL_SIZE
        TOTAL_SIZE += (
            round(
                sum(os.path.getsize(os.path.join(root, file))
                    for root, dirs, files in os.walk(src)
                    for d in dirs if d not in self._exclude_dirs(os.path.join(root, d))
                    for file in files if file not in self._exclude_files(file)) / (UNIT_MULTIPLIER[unit]), 2))

        return TOTAL_SIZE

    @staticmethod
    def _exclude_files(file_name: str) -> bool:
        return any(file_name.endswith(x) for x in DEFAULT_INCLUDED)

    def _copy_tree_with_ignore(self, src, dst, ignore_files: set = None, ignore_dirs: set = None):
        # Initialize the ignore lists
        if ignore_files is None:
            ignore_files = set()
        if ignore_dirs is None:
            ignore_dirs = set()

        # Get the total number of files for the progress bar
        total_files = sum([len(files) for _, _, files in os.walk(src)])

        with tqdm.tqdm(total=total_files, unit='file') as pbar:
            for root, dirs, files in os.walk(src):
                # Exclude the specified file or directory and hidden directories
                if os.path.basename(root) in ignore_dirs or os.path.basename(
                        root) in ignore_files or self._exclude_dirs(root):
                    continue

                # Double check if the directory is Exclude the specified file or directory
                dirs[:] = [d for d in dirs if not self._exclude_dirs(os.path.join(root, d))]

                # List included dirs for debugging
                self._list_included_dirs(dirs)
                included_files = []
                # Exclude shortcut files
                for file_name in files:
                    if not self._exclude_files(file_name):
                        continue

                    # Include the file
                    included_files.append(file_name)

                    # Setup copy2 arguments
                    src_file_path = os.path.join(root, file_name)
                    dst_file_path = os.path.join(dst, os.path.relpath(src_file_path, start=src))
                    dst_file_dir = os.path.dirname(dst_file_path)

                    # Create the directory if it doesn't exist
                    if not os.path.exists(dst_file_dir):
                        os.makedirs(dst_file_dir)

                    # Copy the src
                    shutil.copy2(src_file_path, dst_file_path)
                    pbar.update(1)

                # List included files for debugging
                self._list_included_files(included_files)

    def _get_included_extensions(self) -> Optional[list[str], str]:
        if isinstance(self.__include, list):
            return self.__include
        elif isinstance(self.__include, str):
            if [self.__include]:
                return self.__include
        return DEFAULT_INCLUDED

    @staticmethod
    def _partition_free_space(partition: str, unit='GB') -> float:
        """Get the free space of a partition and format it based on the specified unit."""
        if unit not in UNIT_MULTIPLIER:
            raise ValueError(f"Invalid unit: {unit}")
        try:
            usage = psutil.disk_usage(partition).free
        except Exception as e:
            return f"Error: {e}"

        return usage / UNIT_MULTIPLIER[unit]

    # TODO: it should compare with the TOTAL_SIZE
    def _safe_space(self, partition: str, src: str, unit='GB') -> bool:
        return (self._partition_free_space(partition=partition, unit=unit)
                > TOTAL_SIZE + SAFE_SPACE)

    # TODO
    def _presetup(self):
        # We Need to get total size of the intended backup before we start copying
        for partition in self._handle_particular_partition():
            self._total_dir_size(src=partition)
        pass

    def _list_root_dirs(self, partition: str) -> list:
        return [os.path.join(partition, d) for d in os.listdir(partition) if
                os.path.join(partition, d) not in self._exclude_dirs(os.path.join(partition, d))]

    def _make_copy(self):
        parts = self._handle_particular_partition()
        if isinstance(parts, list):
            for partition in parts:
                for root_dir in self._list_root_dirs(partition):
                    _destination = root_dir if self.__dis == "." else self.__dis
                    backup_dir = os.path.join(_destination, self._create_name())
                    if os.path.exists(_destination) and self._safe_space(partition=partition, src=root_dir):
                        self._copy_tree_with_ignore(src=root_dir, dst=backup_dir)
                        self._setup_copy(src=backup_dir)
                        self._push_to_github(src=backup_dir)
                        self._compress(src=backup_dir)
                    else:
                        raise FileNotFoundError(f"Directory {self.__dis} does not exist")
        """
        First getting all the __partitions
        determine if user wants for all __partitions or specific partition
        and then getting all the files in each partition or particular partition
        ignoring special files like .git
        make a copy of each valid file into a new hidden directory in each partition
        create github repository
        commit changes and push
        """
        pass

    def _compress(self, src: str, style: str = "7z") -> None:
        pass

    def _setup_copy(self, src: str) -> None:
        pass

    def _push_to_github(self, src: str) -> None:
        pass

    def execute(self):
        pass
