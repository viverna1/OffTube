# file_storage.py
import json
import os
import logging

log = logging.getLogger(__name__)


class FileStorage[T]:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def exists(self) -> bool:
        return os.path.exists(self.filepath)

    def load(self) -> T:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            log.exception("Ошибка загрузки: %s", self.filepath)
            raise

    def save_in_file(self, data: T) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    