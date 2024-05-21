# We will apply strategy design pattern
import os
from tqdm import tqdm
import brotli
import rarfile
import zipfile
import tarfile


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

    def compress_directory(self, input_dir, output_file):
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as archive:
            for root, _, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive.write(file_path, arcname=os.path.relpath(file_path, start=input_dir))

    def decompress_archive(self, input_file, output_dir):
        with zipfile.ZipFile(input_file, "r") as archive:
            archive.extractall(output_dir)


class _BrotliStrategy(CompressionStrategy):
    def compress(self, src: str, style: str) -> None:
        raise NotImplementedError

    def decompress(self, src: str, style: str) -> None:
        raise NotImplementedError

    @staticmethod
    def compress_directory(input_dir, output_dir):
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterate over files in the input directory
        for root, _, files in os.walk(input_dir):
            for filename in files:
                # Get the full path of the file
                input_file = os.path.join(root, filename)

                # Read the contents of the file
                with open(input_file, "rb") as f:
                    data = f.read()

                # Compress the file content
                compressed_data = brotli.compress(data)

                # Write the compressed data to the output directory
                output_file = os.path.join(output_dir, filename + ".br")
                with open(output_file, "wb") as f:
                    f.write(compressed_data)

    @staticmethod
    def decompress_directory(input_dir, output_dir):
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterate over files in the input directory
        for root, _, files in os.walk(input_dir):
            for filename in files:
                # Check if the file has a .br extension
                if filename.endswith(".br"):
                    # Get the full path of the file
                    input_file = os.path.join(root, filename)

                    # Read the compressed data from the file
                    with open(input_file, "rb") as f:
                        compressed_data = f.read()

                    # Decompress the data
                    decompressed_data = brotli.decompress(compressed_data)

                    # Write the decompressed data to the output directory
                    output_file = os.path.join(output_dir, filename[:-3])  # Remove the .br extension
                    with open(output_file, "wb") as f:
                        f.write(decompressed_data)


class _TarStrategy(CompressionStrategy):
    def compress(self, src: str, style: str) -> None:
        pass

    def decompress(self, src: str, style: str) -> None:
        pass

    def compress_directory(self, input_dir, output_file):
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(input_dir, arcname=os.path.basename(input_dir))

    def decompress_archive(self, input_file, output_dir):
        with tarfile.open(input_file, "r:gz") as tar:
            tar.extractall(output_dir)


class _RarStrategy(CompressionStrategy):

    def compress(self, src: str, style: str) -> None:
        pass

    def decompress(self, src: str, style: str) -> None:
        pass

    def compress_directory(self, input_dir, output_file):
        with rarfile.RarFile(output_file, "w") as archive:
            for root, _, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive.write(file_path, arcname=os.path.relpath(file_path, start=input_dir))

    def decompress_archive(self, input_file, output_dir):
        with rarfile.RarFile(input_file, "r") as archive:
            archive.extractall(output_dir)


class Compressor:
    STRATEGY_MAP = {"7z": _SevenZStrategy(), "zip": _ZipStrategy(), "rar": _RarStrategy(), "brotli": _BrotliStrategy()}

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
