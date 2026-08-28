# config_storage.py
from .base_storage import Storage

CONFIG_PATH = 'data/config.json'


class ConfigStorage(Storage):
    def _init_empty(self):
        self._data = {}

    def get_setting(self, key):
        return self._data[key]


Config = ConfigStorage(CONFIG_PATH)
