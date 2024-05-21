from abc import ABC, abstractmethod
from utils.log import LogHandler


class _HostsStrategy(ABC):
	def __init__(self) -> None:
		self.log = LogHandler()

	@abstractmethod
	def upload(self) -> None:
		pass

	@abstractmethod
	def download(self) -> None:
		pass

	@abstractmethod
	def update(self) -> None:
		pass

	@abstractmethod
	def setup(self) -> None:
		pass
