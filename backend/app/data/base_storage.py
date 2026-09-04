# base_storage.py
import json
import os
from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)

class Storage(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        self._data: list = []
        self._load()
    
    def _load(self):
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except (json.JSONDecodeError, OSError):
            log.error(f"Ошибка загрузки {self.filepath}:", exc_info=True)
    
    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self._data
    