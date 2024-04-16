from functools import wraps
from typing import Callable
import os
from utils.constants import SUPPORTED_COMPRESS_EXTENSIONS


def run_once(func) -> Callable:
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not wrapper.has_run:
			wrapper.has_run = True
			return func(*args, **kwargs)
		raise RuntimeError(f"{func.__name__} can only be called once")

	wrapper.has_run = False
	return wrapper


def valid_src(src: str) -> bool:
	return not any(src.endswith(x) for x in SUPPORTED_COMPRESS_EXTENSIONS) and os.path.isdir(src)
