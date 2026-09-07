# config_storage.py
import logging
from typing import Any

from app.infrastructure.file_storage import FileStorage

log = logging.getLogger(__name__)

CONFIG_PATH = 'data/config.json'


class ConfigStorage(FileStorage[dict]):
    _data: dict
    
    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self._data = self.load()

    def get_setting(self, key: str) -> Any:
        return self._data.get(key)

    def set_setting(self, key: str, value: Any) -> None:
        if self.get_setting(key) is None:
            log.error("Key %s not found in config", key)
            return
        self._data[key] = value
        self.save(self._data)

    def get_data(self):
        return self._data

    @staticmethod
    def create():
        return ConfigStorage(CONFIG_PATH)
        

configStorage = ConfigStorage.create()