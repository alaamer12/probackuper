from .base_strategy import _HostsStrategy


class _GoggleDriveStrategy(_HostsStrategy):
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
		pass
