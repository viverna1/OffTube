# cache_storage.py
from typing import Any

from app.infrastructure.file_storage import FileStorage

# ??? Просто информация для просвещения
# ? Сравнение паттернов
# ? Название	Паттерн	Когда использовать
# ? CacheRepository	Repository	Когда хотите абстрагировать источник данных
# ? CacheManager	Manager/Facade	Когда управляете сложной логикой кэша
# ? FileCacheStore	Store	Когда акцент на хранении данных
# ? CachedFileStorage	Decorator	Когда добавляете кэш к существующему классу
# ? PersistentCache	-	Когда хотите простое, понятное название


class CacheStorage(FileStorage):
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
        self._save()

    def set_batch(self, new_data: dict) -> None:
        self._storage.update(new_data)
        self._save()

    def delete(self, key: str) -> None:
        if not self.has(key): return
        del self._storage[key]
        self._save()

    def get_all(self) -> dict[str, Any]:
        return self._storage

    # other
    def _save(self) -> None:
        super().save_in_file(self._storage)

    def clear_cache(self) -> None:
        self._storage = {}
        self._save()
