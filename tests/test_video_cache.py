# test_video_cache.py
import pytest

from app.domain.video import Video
from app.infrastructure.repository.cache_repository import CacheRepository
from app.infrastructure.repository.video_cache import VideoCache


def create_video(number: str):
    return Video(
        id=number,
        name=f"vid{number}",
        filename=f"vid{number}.mp4",
        path=f"vids/vid{number}.mp4",
        thumbnail=f"thumb/vid{number}.mp4.jpg",
        duration=1.5
    )


# ==================== Fixtures ====================

@pytest.fixture
def mock_cache_repository(mocker):
    mock_load = mocker.patch.object(CacheRepository, 'load', return_value={})
    mock_save = mocker.patch.object(CacheRepository, '_save')
    return mock_load, mock_save

@pytest.fixture
def cache_repository(mock_cache_repository):
    return CacheRepository("")

@pytest.fixture
def video_cache(cache_repository):
    return VideoCache(cache_repository)


# ==================== Tests ====================

def test_set_and_get(video_cache, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    video = create_video("1")
    video_cache.set_video(video)

    assert video_cache.get_by_id("1") == video

    mock_save.assert_called_once()

def test_add_videos(video_cache, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    video1 = create_video("1")
    video2 = create_video("2")
    video_cache.add_videos([video1, video2])
    assert video_cache.get_by_id(video1.id) == video1
    assert video_cache.get_by_id(video2.id) == video2
    mock_save.assert_called()

def test_delete(video_cache, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository

    video = create_video("2")
    video_cache.set_video(video)
    video_cache.delete("2")
    assert video_cache.get_by_id("2") is None
    
    mock_save.assert_called()

def test_invalid_id(video_cache, mock_cache_repository):
    assert video_cache.get_by_id("1") is None

def test_delete_nonexistent(video_cache, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    video_cache.delete("999")

    mock_save.assert_not_called()
