# config_storage.py
from .base_storage import Storage

CONFIG_PATH = 'data/config.json'


class ConfigStorage(Storage):
    def get_all(self):
        return self._data[0]

    def get_setting(self, key):
        return self._data[0].get(key)


Config = ConfigStorage(CONFIG_PATH)
