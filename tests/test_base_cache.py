# test_base_cache.py
import pytest

from app.infrastructure.repository.cache_repository import CacheRepository


# ==================== Fixtures ====================

@pytest.fixture
def mock_cache_repository(mocker):
    mock_load = mocker.patch.object(CacheRepository, 'load', return_value={})
    mock_save = mocker.patch.object(CacheRepository, '_save')
    return mock_load, mock_save

@pytest.fixture
def cache_repository(mock_cache_repository):
    return CacheRepository("")


# ==================== Tests ====================

def test_get_set(cache_repository, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    cache_repository.set("key", "value")
    assert cache_repository.get("key") == "value"

    mock_save.assert_called()

def test_delete(cache_repository, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    cache_repository.set("key", "value")
    cache_repository.delete("key")
    assert not cache_repository.has("key")

    mock_save.assert_called()

def test_set_batch(cache_repository, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    cache_repository.set_batch({"key1": "value1", "key2": "value2"})
    assert cache_repository.get("key1") == "value1"
    assert cache_repository.get("key2") == "value2"

    mock_save.assert_called()


def test_delete_nonexistent(cache_repository, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    cache_repository.delete("999")

    mock_save.assert_not_called()