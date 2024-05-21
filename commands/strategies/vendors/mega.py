import os

from mega import Mega
from dotenv import load_dotenv

from .base_strategy import _HostsStrategy


class _MegaStrategy(_HostsStrategy):
	def __init__(self, src: str, email: str, password: str):
		super().__init__()
		self.cwd = src
		self.__email = email
		self.__password = password

	def upload(self) -> None:
		pass

	def download(self) -> None:
		pass

	def update(self) -> None:
		pass

	def setup(self) -> None:
		load_dotenv()
		mega = Mega()

		m = mega.login(os.getenv("MEGA_EMAIL_ACCOUNT"), os.getenv("MEGA_EMAIL_PASSWORD"))
		quota = m.get_quota()
		details = m.get_user()
		print(details)
		print(quota)
