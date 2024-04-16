import win32file
import win32event
import win32con


class DirectoryMonitor:
	def __init__(self, directory):
		self.directory = directory
		self.change_handle = None

	def start_monitoring(self):
		self.change_handle = win32file.FindFirstChangeNotification(
			self.directory, 0, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
		)
		try:
			while True:
				result = win32event.WaitForSingleObject(self.change_handle, win32event.INFINITE)
				if result == win32event.WAIT_OBJECT_0:
					print("Directory changed!")
					try:
						action, file_path = win32file.ReadDirectoryChangesW(
							self.change_handle, 1024, True, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE, None, None
						)[0]
						print(f"Action: {action}, File: {file_path}")
					except Exception as e:
						print(f"Error: {e}")
					win32file.FindNextChangeNotification(self.change_handle)
		finally:
			win32file.FindCloseChangeNotification(self.change_handle)

	def stop_monitoring(self):
		if self.change_handle:
			win32file.FindCloseChangeNotification(self.change_handle)
			self.change_handle = None


#
# # Example usage
# directory = r"D:\ups\ideaProjects\the app\thanwyaIdea\ReactTests\projects"
# monitor = DirectoryMonitor(directory)
# monitor.start_monitoring()
