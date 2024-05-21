from utils.constants import GITIGNORE
import subprocess
from .base_strategy import _HostsStrategy
from typing import Union, List
import os
import sys


class _GithubStrategy(_HostsStrategy):
	def __init__(self, src: str, publication: str = "--private") -> None:
		super().__init__()
		self.setup()
		self.__init = False
		self.__cwd = src
		self.__verified_repo_name = None
		self.__repo_url = None
		self.__publication = publication

	def __repr__(self):
		return f"{self.__class__.__name__}({self.__cwd!r})"

	def upload(self) -> None:
		if not self.__init:
			self.setup()
		try:
			_message = ""
			self.__repo_url = f"https://github.com/{self._get_username()}/" f"{self.__verified_repo_name}.git"
			self._shell(["git", "add", "."])
			self._shell(["git", "commit", "-m", _message])
			self._shell(["git", "branch", "-M", "main"])
			self._shell(["git", "remote", "add", "origin", self.__repo_url])
			self._shell(["git", "push", "-u", "origin", "main"])
		except subprocess.CalledProcessError as e:
			print(f"Failed to commit and push: {e}")
		except Exception as e:
			print(f"Failed to commit and push: {e}")

	def download(self) -> None:
		if self.__repo_url is not None:
			try:
				self._shell(["git", "clone", self.__repo_url])
			except subprocess.CalledProcessError as e:
				print(f"Failed to clone: {e}")

	def update(self) -> None:
		raise NotImplementedError("Update method is not implemented")

	@staticmethod
	def _verify_directory_name(_directory_name):
		if " " in _directory_name:
			print("Invalid directory name.")
			print("Directory name should not contain any spaces.")
			print("Trying to fix it...")
			_directory_name = _directory_name.replace(" ", "_")
			print(f"Directory name: {_directory_name}")
			return _directory_name
		return _directory_name

	def _shell(self, command: Union[str, List[str]], capture_output: bool = False) -> subprocess.CompletedProcess[str]:
		if capture_output:
			return subprocess.run(command, check=True, cwd=self.__cwd, capture_output=True, text=True, shell=True)
		return subprocess.run(command, check=True, cwd=self.__cwd, shell=True)

	def _check_authorized_user(self):
		"""Check if authorized user is logged in"""
		try:
			_result = self._shell(["gh", "auth", "status"], capture_output=True)
			if not _result.stdout.find("Logged in to github.com account"):
				print("You are not logged in to GitHub.")
				print("Please __log in and try again.")
				sys.exit()
		except subprocess.CalledProcessError:
			pass

	def _get_username(self):
		if self._check_authorized_user():
			_result = self._shell(["gh", "auth", "status"], capture_output=True)
			first_index = _result.stdout.find("account") + len("account") + 1
			last_index = _result.stdout.find("(") - 1
			return _result.stdout[first_index:last_index]
		raise Exception("You are not logged in to GitHub.")

	def setup(self) -> None:
		if not self.__init:
			self.__init = True

			# Create gitignore file
			# Check of existing .git
			if not os.path.exists(".git"):
				self._shell(["git", "init"])

			gitignore = os.path.join(self.__cwd, ".gitignore")
			if not os.path.exists(gitignore):
				with open(gitignore, "w") as gitignore_file:
					gitignore_file.write(GITIGNORE)

			repo_name = os.path.basename(self.__cwd)
			self.__verified_repo_name = self._verify_directory_name(repo_name)

			# Create a repo on GitHub
			try:
				subprocess.run(["gh", "repo", "create", self.__verified_repo_name, self.__publication], cwd=self.__cwd)
			except subprocess.CalledProcessError as e:
				print(f"Failed to create repo on GitHub: {e}")
			# pass
		else:
			print("Already initialized.")
