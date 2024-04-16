class BackupException:
	class BackupNotFoundError(FileNotFoundError):
		pass

	class CorruptedBackupError(IOError):
		pass
