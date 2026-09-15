# cache_repository.py
from typing import Any

from app.infrastructure.repository.json_repository import JsonRepository


class CacheRepository(JsonRepository):
    def __init__(self, filepath: str):
        super().__init__(filepath=filepath)
        self._cache: dict = self.load()

    # getters
    def get(self, key: str) -> Any | None:
        return self._cache.get(key, None)

    def has(self, key: str) -> bool:
        return self._cache.get(key, None) is not None

    # setters
    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._save()

    def set_batch(self, new_data: dict) -> None:
        self._cache.update(new_data)
        self._save()

    def delete(self, key: str) -> None:
        if not self.has(key): return
        del self._cache[key]
        self._save()

    def get_all(self) -> dict[str, Any]:
        return self._cache

    # other
    def _save(self) -> None:
        super().save_in_file(self._cache)

    def clear_cache(self) -> None:
        self._cache = {}
        self._save()
