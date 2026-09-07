# video_cache.py
from typing import Any

from app.infrastructure.file_storage import FileStorage

VIDEOS_PATH = 'data/videos.json'


class BaseCache(FileStorage):
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        self._storage: dict = self.load()

    # getters
    def get(self, key: str) -> Any | None:
        return self._storage.get(key, None)

    def has(self, key: str) -> bool:
        return self._storage.get(key, None) is not None

    # setters
    def set(self, key: str, value: Any) -> None:
        self._storage[key] = value
        self.save()

    def set_batch(self, new_data: dict) -> None:
        self._storage.update(new_data)
        self.save()

    def delete(self, key: str) -> None:
        if not self.has(key): return
        del self._storage[key]
        self.save()

    def get_all(self) -> dict[str, Any]:
        return self._storage

    # other
    def save(self) -> None:
        super().save_in_file(self._storage)

    def clear_cache(self) -> None:
        self._storage = {}
        self.save()


# class old:
#     def get(self, key: str) -> Any | None:
#         return self.get_all().get(key, None)

#     def has(self, key: str) -> bool:
#         return self.get_all().get(key, None) is not None

#     def set(self, key: str, value: Any) -> None:
#         new_data = self.get_all()
#         new_data[key] = value
#         self.save(new_data)

#     def get_all(self) -> dict:
#         return self.load()

#     def clear_cache(self) -> None:
#         self.save([])
