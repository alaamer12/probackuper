import os
from .strategies.hosts import HostManager
from utils.constants import SAFE_UPLOAD_SIZE
from commands.handler.base_command import ICommand


class Upload(ICommand):
	def __init__(self, src, host: str = "github"):
		self.src = src
		self.host = host
		if not self._validate():
			return

	def _validate(self):
		# Check if the file is bigger than 1 GB
		if os.path.getsize(self.src) > SAFE_UPLOAD_SIZE:
			# Ask the user if they want to continue
			i = (
				input(f"File {self.src} is bigger than {SAFE_UPLOAD_SIZE} bytes, do you want to continue? (y/n): ")
				.strip()
				.lower()
			)
			while i != "y" and i != "n":
				print("Invalid input. Please enter 'y' or 'n'.")
			if i != "y":
				return False
		return True

	def execute(self):
		# Upload the file to the host
		host = HostManager(host=self.host, src=self.src)
		host.upload()
