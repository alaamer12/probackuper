DEFAULT_INCLUDED = [
	".py",
	".txt",
	".md",
	".jpg",
	".png",
	".docx",
	".pdf",
	".epub",
	".doc",
	".pptx",
	".ppt",
	".xlsx",
	".xls",
	".mp3",
	".m4a",
	".mp4",
	".mov",
	".avi",
	".mkv",
	".json",
	".js",
	".css",
	".html",
	".xml",
	".csv",
]

# DEFAULT_EXCLUDED = [".lnk",".webm", ".iso", ".rar",
# ".zip", ".gz", ".tar", ".gz", ".bz2", ".xz",
# ".7z", ".exe", ".dll", ".sys", ".lnk", ".msi",
# ".pdf", ".docx", ".pptx", ".xlsx", ".apk",
# ".deb", ".rpm", ".iso", ".dmg", ".app"]

EXCLUDED_DIRS = [".git", ".venv", "venv", "node_modules", ".pnpm-store", ".DS_Store", ".idea", ".vscode"]

UNIT_MULTIPLIER = {"GB": 1e9, "MB": 1e6, "Bytes": 1}

SAFE_SPACE = 10

SUPPORTED_COMPRESS_EXTENSIONS = ["7z", "zip", "rar", "tar", "rar4"]

DEFAULT_UNIT = "GB"

SAFE_UPLOAD_SIZE = 1024 * 1024 * 1024

GITIGNORE = """
# Operating System Files
.DS_Store
Thumbs.db
desktop.ini

# IDE/Editor Files
.idea/
.vscode/
*.suo
*.ntvs*
*.njsproj
*.sln
*.swp
*~

# Build Output
node_modules/
dist/
build/
*.o
*.obj
*.class

# Dependency Directories
vendor/
jspm_packages/
typings/
*.jar
*.war

# Logs and Temporary Files
*.__log
*.tmp
*.temp

# System Files
*.dll
*.exe
*.pdb
*.lib
*.so
*.dylib

# Configuration Files
.env
.DS_Store
.project
.classpath
.settings/

# IDE/Editor Specific
.idea/
.vscode/
*.sublime-project
*.sublime-workspace
*.idea/

# Miscellaneous
.dockerignore
.npmignore
.babelrc
.eslintrc
.gitattributes

# Custom Logs or Data Files
# Add any other file or directory specific to your project
"""
