from base_command import ICommand
import psutil
import os
from enum import Enum
from typing import Optional, List, Any, Union, Tuple, List
import shutil
import datetime
import sys
import tqdm
import subprocess
import logging
import string
import random
DEFAULT_FILTERS = [""]


# TODO: add support for partial backup
# TODO: add datetime, logging, error handling

class Backup(ICommand):
    def __init__(self, __partial=None, __filter: Optional[List[str], str] = None):
        self.partitions = []
        self.__partial = __partial
        self.__filter = __filter


    def _create_name(self) -> str:
        return "$bkup".join(random.choices(string.ascii_uppercase + string.digits, k=10)[0:4])
    def _get_mount_points(self) -> list[str]:
        for partition in psutil.disk_partitions():
            if partition.fstype != "NTFS":
                continue
            self.partitions.append(partition)
        return self.partitions

    def _handle_partial(self, partition: str) -> tuple[bool, str, any]:
        if not isinstance(partition, str):
            return False, partition, "Partition should be a string"
        try:
            all_partitions = self._get_mount_points()
            if partition.upper() not in all_partitions:
                return False, partition, "Partition is not mounted"
            return True, partition, "Partition is mounted"
        except ValueError as e:
            return False, partition, e
        except Exception as e:
            print(e)
            return False, partition, e

    def hide_directory(self, path) -> None:
        try:
            # Set the hidden attribute
            os.system('attrib +h "{}"'.format(path))
            print("Directory '{}' is now hidden.".format(path))
        except Exception as e:
            print("Error:", e)

    def unhide_directory(self, path):
        try:
            # Remove the hidden attribute
            os.system('attrib -h "{}"'.format(path))
            print("Directory '{}' is now visible.".format(path))
        except Exception as e:
            print("Error:", e)

    def _is_hidden(self, path):
        try:
            # Get file attributes
            attrs = os.stat(path).st_file_attributes
            # Check if the hidden attribute is set
            return attrs & 2 != 0
        except Exception as e:
            print("Error:", e)
            return False

    def _get_partition_dirs(self) -> Union[List[Tuple[str, List[str]]], List[Tuple[str, str]]]:
        partition_dirs = []
        if self.__partial:
            success, partition, _ = self._handle_partial(self.__partial)
            if success:
                dirs = self._fetch_dirs(partition)
                partition_dirs.append((partition, dirs))
        else:
            for partition in self._get_mount_points():
                dirs = self._fetch_dirs(partition)
                partition_dirs.append((partition, [dirs]))
        return partition_dirs

    def _fetch_dirs(self, partition: str) -> List[str]:
        dirs = []
        for _dir in os.listdir(partition):
            dir_path = os.path.join(partition, _dir)
            if self._filter_dirs(dir_path):
                dirs.append(dir_path.encode("utf-8").decode("utf-8"))
        return dirs

    def _filter_dirs(self, dir_path: str) -> bool:
        return os.path.isdir(dir_path) and not self._is_hidden(dir_path) and not dir_path.endswith('.lnk')
    def _walk(self) -> list[str]:
        for dir in self._get_partition_dirs():
            for root, dirs, files in os.walk(dir):
                if self.__filter:
                    dirs[:] = [d for d in dirs if d in self.__filter]
                yield root, dirs, files


    def _get_filtered_files(self) -> Optional[list[str], str]:
        if isinstance(self.__filter, list) or isinstance(self.__filter, str):
            if self.__filter:
                return self.__filter
        return DEFAULT_FILTERS

    def _filter(self):
        pass

    def _make_copy(self):
        for partition, _ in self._get_partition_dirs():
            path = os.path.join(partition, self._create_name())
            if not os.path.exists(path):
                os.mkdir(path)
            # for root, dirs, files in self._walk():
            #     for file in files:
            #         src = os.path.join(root, file)
            #         dst = os.path.join(path, file)
            #         shutil.copy(src, dst)

    def execute(self):
        pass
