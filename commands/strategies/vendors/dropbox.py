import os
import dropbox
from dotenv import load_dotenv

from .base_strategy import _HostsStrategy


class _DropboxStrategy(_HostsStrategy):
	def __init__(self, src: str):
		super().__init__()
		self.cwd = src

	def upload(self) -> None:
		pass

	def download(self) -> None:
		pass

	def update(self) -> None:
		pass

	def setup(self) -> None:
		load_dotenv()
		dbx = dropbox.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))
		print(dbx.users_get_current_account())
