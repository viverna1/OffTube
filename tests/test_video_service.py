# test_videos_cache.py
import pytest

from app.domain.video import Video
from app.infrastructure.repository.cache_repository import CacheRepository
from app.infrastructure.repository.video_cache import VideoCache
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

@pytest.fixture
def video_service(video_cache, mock_video_exists):
    return VideoService(video_cache)

# ==================== Tests ====================

def test_add_and_get(video_service, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    video = create_video("1")

    video_service.add_video(video)

    assert video_service.get_video("1") == video
    mock_save.assert_called_once()

def test_add_videos(video_service, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    video1 = create_video("1")
    video2 = create_video("2")

    video_service.add_videos([video1, video2])

    assert video_service.get_video(video1.id) == video1
    assert video_service.get_video(video2.id) == video2
    mock_save.assert_called()

def test_banch_videos(video_service, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    video1 = create_video("1")
    video2 = create_video("2")
    video3 = create_video("3")

    video_service.add_videos([video1, video2, video3])

    videos1 = video_service.get_banch_videos(0, 5)
    assert len(videos1) == 3
    assert videos1 == [video1, video2, video3]

    videos1 = video_service.get_banch_videos(0, 2)
    assert len(videos1) == 2
    assert videos1 == [video1, video2]

    videos1 = video_service.get_banch_videos(1, 1)
    assert len(videos1) == 1
    assert videos1 == [video2]

    videos1 = video_service.get_banch_videos(1, 2)
    assert len(videos1) == 2
    assert videos1 == [video2, video3]

def test_delete(video_service, mock_cache_repository):
    mock_load, mock_save = mock_cache_repository
    video = create_video("2")

    video_service.add_video(video)
    video_service.delete("2")

    assert video_service.get_video("2") is None
    mock_save.assert_called()
