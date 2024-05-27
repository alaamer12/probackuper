from typing import Optional, List
from commands.handler.base_command import ICommand

TOTAL_SIZE = 0

# Only Windows supported for now

class Backup(ICommand):
	def __init__(
		self, __particular_partition=None, __include: Optional[List[str], str] = None, __dis: str = "."
	) -> None:
		"""
		Initialize the Backup command.

		Parameters:
		- __particular_partition: Optional[str]
		    The particular partition to backup.
		- __include: Optional[List[str], str]
		    List of directories or files to include in the backup.
		- __dis: str
		    The destination directory for the backup.
		"""
		self.__dis = None
		self.__system_partition = None
		self.__particular_partition = None
		self.__include = None
		...

	@staticmethod
	def _create_name() -> str:
		"""
		Generate a unique name for the backup.

		Returns:
		- str: The generated name.
		"""
		...

	def _handle_particular_partition(self) -> Optional[List[str], tuple[bool, str, any]]:
		"""
		Get the list of partitions to backup.

		Returns:
		- Optional[List[str], tuple[bool, str, any]]: The list of partitions or an error tuple.
		"""
		...

	@staticmethod
	def _hide_directory(path) -> None:
		"""
		Hide a directory.

		Parameters:
		- path: str
		    The path of the directory to hide.
		"""
		...

	@staticmethod
	def _unhide_directory(path):
		"""
		Unhide a directory.

		Parameters:
		- path: str
		    The path of the directory to unhide.
		"""
		...

	@staticmethod
	def _is_hidden(path):
		"""
		Check if a directory is hidden.

		Parameters:
		- path: str
		    The path of the directory to check.

		Returns:
		- bool: True if the directory is hidden, False otherwise.
		"""
		...

	@staticmethod
	def _list_included_dirs(_included_dirs) -> None:
		"""
		List included directories for debugging purposes.

		Parameters:
		- _included_dirs: List[str]
		    The list of included directories.
		"""
		...

	@staticmethod
	def _list_included_files(_included_files) -> None:
		"""
		List included files for debugging purposes.

		Parameters:
		- _included_files: List[str]
		    The list of included files.
		"""
		...

	def _exclude_dirs(self, path) -> bool:
		"""
		Check if a directory should be excluded from the backup.

		Parameters:
		- path: str
		    The path of the directory to check.

		Returns:
		- bool: True if the directory should be excluded, False otherwise.
		"""
		...

	def _total_dir_size(self, src: str, unit: str = "GB") -> float:
		"""
		Calculate the total size of a directory.

		Parameters:
		- src: str
		    The path of the directory.
		- unit: str
		    The unit for the size calculation (default is "GB").

		Returns:
		- float: The total size of the directory.
		"""
		...

	@staticmethod
	def _exclude_files(file_name: str) -> bool:
		"""
		Check if a file should be excluded from the backup.

		Parameters:
		- file_name: str
		    The name of the file to check.

		Returns:
		- bool: True if the file should be excluded, False otherwise.
		"""
		...

	def _copy_tree_with_ignore(self, src, dst, ignore_files: set = None, ignore_dirs: set = None):
		"""
		Copy a directory tree, ignoring specified files and directories.

		Parameters:
		- src: str
		    The source directory.
		- dst: str
		    The destination directory.
		- ignore_files: set
		    Set of files to ignore.
		- ignore_dirs: set
		    Set of directories to ignore.
		"""
		...

	def _get_included_extensions(self) -> Optional[list[str], str]:
		"""
		Get the list of included extensions.

		Returns:
		- Optional[list[str], str]: The list of included extensions or an error message.
		"""
		...

	@staticmethod
	def _partition_free_space(partition: str, unit="GB") -> float:
		"""
		Get the free space of a partition.

		Parameters:
		- partition: str
		    The partition path.
		- unit: str
		    The unit for the size calculation (default is "GB").

		Returns:
		- float: The free space of the partition.
		"""
		...

	def _safe_space(self, partition: str, src: str, unit="GB") -> bool:
		"""
		Check if there is enough free space on the partition for the backup.

		Parameters:
		- partition: str
		    The partition path.
		- src: str
		    The source directory.
		- unit: str
		    The unit for the size calculation (default is "GB").

		Returns:
		- bool: True if there is enough space, False otherwise.
		"""
		...

	def _presetup(self):
		"""
		Perform pre-setup tasks before starting the backup.
		"""
		...

	def _list_root_dirs(self, partition: str) -> list:
		"""
		List root directories of a partition.

		Parameters:
		- partition: str
		    The partition path.

		Returns:
		- list: List of root directories.
		"""
		...

	def _make_copy(self):
		"""
		Make a copy of the specified directories.
		"""
		...

	def _compress(self, src: str, style: str = "7z") -> None:
		"""
		_BaseCompress the backup directory.

		Parameters:
		- src: str
		    The source directory to compress.
		- style: str
		    The compression style (default is "7z").
		"""
		...

	def _setup_copy(self, src: str) -> None:
		"""
		Set up the backup copy.

		Parameters:
		- src: str
		    The source directory.
		"""
		...

	def _push_to_github(self, src: str) -> None:
		"""
		Push the backup to GitHub.

		Parameters:
		- src: str
		    The source directory.
		"""
		...

	def execute(self):
		"""
		Execute the backup command.
		"""
		...
