# config_storage.py
import logging
from typing import Any

from app.infrastructure.file_storage import FileStorage

log = logging.getLogger(__name__)


class ConfigStorage():
    def __init__(self, file_storage: FileStorage) -> None:
        self._file_storage = file_storage

    def get_setting(self, key: str) -> Any:
        return self._file_storage.load().get(key)

    def set_setting(self, key: str, value: Any) -> None:
        if self.get_setting(key) is None:
            log.error("Key %s not found in config", key)
            return
        new_data = self._file_storage.load()
        new_data[key] = value
        self._file_storage.save_in_file(new_data)

    def get_all(self):
        return self._file_storage.load()
    