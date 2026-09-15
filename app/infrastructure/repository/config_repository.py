# config_repository.py
import logging
from typing import Any

from app.infrastructure.repository.json_repository import JsonRepository

log = logging.getLogger(__name__)


class ConfigRepository():
    def __init__(self, json_repository: JsonRepository) -> None:
        self._json_repository = json_repository

    def get_setting(self, key: str) -> Any:
        return self._json_repository.load().get(key)

    def set_setting(self, key: str, value: Any) -> None:
        if self.get_setting(key) is None:
            log.error("Key %s not found in config", key)
            return
        new_data = self._json_repository.load()
        new_data[key] = value
        self._json_repository.save_in_file(new_data)

    def get_all(self):
        return self._json_repository.load()
    