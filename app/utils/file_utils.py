# file_utils.py
import os

def get_file_name(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]

def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)


def file_exists(file_path: str) -> int:
    return os.path.exists(file_path)
