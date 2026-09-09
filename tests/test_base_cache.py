# test_base_cache.py
import pytest

from app.infrastructure.cache_storage import CacheStorage


# ==================== Fixtures ====================

@pytest.fixture
def mock_cache_storage(mocker):
    mock_load = mocker.patch.object(CacheStorage, 'load', return_value={})
    mock_save = mocker.patch.object(CacheStorage, '_save')
    return mock_load, mock_save


@pytest.fixture
def cache_storage(mock_cache_storage):
    return CacheStorage("")


# ==================== Tests ====================

def test_get_set(cache_storage, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage

    cache_storage.set("key", "value")
    assert cache_storage.get("key") == "value"

    mock_save.assert_called()

def test_delete(cache_storage, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage

    cache_storage.set("key", "value")
    cache_storage.delete("key")
    assert not cache_storage.has("key")

    mock_save.assert_called()

def test_set_batch(cache_storage, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage

    cache_storage.set_batch({"key1": "value1", "key2": "value2"})
    assert cache_storage.get("key1") == "value1"
    assert cache_storage.get("key2") == "value2"

    mock_save.assert_called()


def test_delete_nonexistent(cache_storage, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage

    cache_storage.delete("999")

    mock_save.assert_not_called()