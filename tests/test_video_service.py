# test_videos_cache.py
import pytest

from app.domain.video import Video
from app.infrastructure.cache_storage import CacheStorage
from app.infrastructure.video_cache import VideoCache
from app.application.video_service import VideoService


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
def mock_video_exists(mocker):
    return mocker.patch.object(Video, 'exists', return_value=True)

@pytest.fixture
def mock_cache_storage(mocker):
    mock_load = mocker.patch.object(CacheStorage, 'load', return_value={})
    mock_save = mocker.patch.object(CacheStorage, '_save')
    return mock_load, mock_save

@pytest.fixture
def cache_storage(mock_cache_storage):
    return CacheStorage("")

@pytest.fixture
def video_cache(cache_storage):
    return VideoCache(cache_storage)

@pytest.fixture
def video_service(video_cache, mock_video_exists):
    return VideoService(video_cache)


# ==================== Tests ====================

def test_add_and_get(video_service, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage
    video = create_video("1")

    video_service.add_video(video)

    assert video_service.get_video("1") == video
    mock_save.assert_called_once()


def test_add_videos(video_service, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage
    video1 = create_video("1")
    video2 = create_video("2")

    video_service.add_videos([video1, video2])

    assert video_service.get_video(video1.id) == video1
    assert video_service.get_video(video2.id) == video2
    mock_save.assert_called()


def test_delete(video_service, mock_cache_storage):
    mock_load, mock_save = mock_cache_storage
    video = create_video("2")

    video_service.add_video(video)
    video_service.delete("2")

    assert video_service.get_video("2") is None
    mock_save.assert_called()
