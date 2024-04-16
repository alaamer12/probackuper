import functools
from .helpers.directory_monitor import DirectoryMonitor
from .log import LogHandler


class Diagonalise:
	def __init__(self, directory):
		self.directory = directory
		self.director_monitor = DirectoryMonitor(self.directory)
		self.log = LogHandler()

	def cleanup(self, func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception as e:
				self.log.log_it(e, level="error")
				return func(*args, **kwargs)

		return wrapper
