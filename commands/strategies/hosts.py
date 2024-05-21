import os

from utils.helper import run_once, valid_src
from .vendors.discord import _DiscordStrategy
from .vendors.github import _GithubStrategy
from .vendors.google_drive import _GoggleDriveStrategy
from .vendors.dropbox import _DropboxStrategy

"""We need to implement simple db to save states of hosts."""


class HostManager:
	# TODO; Add support for other hosts
	# TODO; Add src argument
	STRATEGY_MAP = {
		"github": _GithubStrategy,
		"discord": _DiscordStrategy,
		"google-drive": _GoggleDriveStrategy,
		"dropbox": _DropboxStrategy,
	}

	def __init__(self, src: str, host: str):
		# Check first if src is valid
		if not valid_src(src):
			if not os.path.isdir(src):
				raise Exception("Source is not valid")
			raise Exception("Source is compressed cant upload, decompress first and try again")
		self.strategy = self.STRATEGY_MAP.get(host)(src=src)

	@run_once
	def download(self) -> None:
		self.strategy.download()

	@run_once
	def upload(self) -> None:
		self.strategy.upload()

	@run_once
	def update(self) -> None:
		self.strategy.update()

	@run_once
	def setup(self) -> None:
		self.strategy.setup()
