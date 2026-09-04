# base_storage.py
import json
import os
from abc import ABC, abstractmethod

class Storage(ABC):
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = None
        self._load()
    
    def _load(self):
        if not os.path.exists(self.filepath):
            self._init_empty()
            return
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Ошибка загрузки {self.filepath}: {e}")
            self._init_empty()
    
    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self._data
    
    @abstractmethod
    def _init_empty(self):
        pass
    