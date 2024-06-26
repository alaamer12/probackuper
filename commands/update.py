from .strategies.hosts import HostManager
from commands.handler.base_command import ICommand


class Update(ICommand):
	def __init__(self, src, host: str = "github"):
		self.src = src
		self.host = host

	def execute(self):
		host = HostManager(host=self.host, src=self.src)
		host.update()
