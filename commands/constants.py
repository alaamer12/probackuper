DEFAULT_INCLUDED = [".py", ".txt", ".md", ".jpg", ".png", ".docx", ".pdf", ".epub", ".doc", ".pptx", ".ppt", ".xlsx",
                    ".xls", ".mp3", ".m4a", ".mp4", ".mov", ".avi", ".mkv", ".json", ".js", ".css", ".html", ".xml",
                    ".csv"]
# DEFAULT_EXCLUDED = [".lnk",".webm", ".iso", ".rar", ".zip", ".gz", ".tar", ".gz", ".bz2", ".xz", ".7z", ".exe", ".dll", ".sys", ".lnk", ".msi", ".pdf", ".docx", ".pptx", ".xlsx", ".apk", ".deb", ".rpm", ".iso", ".dmg", ".app"]
EXLUDED_DIRS: list = [".git", ".venv", "venv", "node_modules", ".pnpm-store", ".DS_Store", ".idea", ".vscode"]
UNIT_MULTIPLIER = {'GB': 1e9, 'MB': 1e6, 'Bytes': 1}
SAFE_SPACE = 10
UNIT = "GB"
