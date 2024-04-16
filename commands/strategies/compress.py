# We will apply strategy design pattern
import os
from tqdm import tqdm


class CompressionStrategy:
	def compress(self, src: str, style: str) -> None:
		pass

	def decompress(self, src: str, style: str) -> None:
		pass


class _SevenZStrategy(CompressionStrategy):
	from py7zr import SevenZipFile

	def compress_directory(self, input_dir, output_file):
		with self.SevenZipFile(output_file, "w") as archive:
			files = []
			for root, _, files in os.walk(input_dir):
				files.extend(files)
			with tqdm(total=len(files), desc="Compressing files") as pbar:
				for root, _, files in os.walk(input_dir):
					for file in files:
						file_path = os.path.join(root, file)
						archive.write(file_path, arcname=os.path.relpath(file_path, start=input_dir))
						pbar.update(1)

	def decompress_archive(self, input_file, output_dir):
		with self.SevenZipFile(input_file, "r") as archive:
			files = archive.namelist()
			with tqdm(total=len(files), desc="Decompressing files") as pbar:
				archive.extractall(path=output_dir)
				pbar.update(len(files))


class _ZipStrategy(CompressionStrategy):
	def compress(self, src: str, style: str) -> None:
		raise NotImplementedError

	def decompress(self, src: str, style: str) -> None:
		raise NotImplementedError


class _RarStrategy(CompressionStrategy):
	def compress(self, src: str, style: str) -> None:
		pass

	def decompress(self, src: str, style: str) -> None:
		pass


class Compressor:
	STRATEGY_MAP = {"7z": _SevenZStrategy(), "zip": _ZipStrategy(), "rar": _RarStrategy()}

	def compress(self, src: str, style: str) -> None:
		strategy = self.STRATEGY_MAP.get(style)
		if strategy is None:
			raise ValueError(f"Unsupported compression style: {style}")

		strategy.compress(src, style)

	def decompress(self, src: str, style: str) -> None:
		strategy = self.STRATEGY_MAP.get(style)
		if strategy is None:
			raise ValueError(f"Unsupported compression style: {style}")

		strategy.decompress(src, style)
