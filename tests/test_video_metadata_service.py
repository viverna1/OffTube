# test_video_metadata_service.py
import pytest
from unittest.mock import MagicMock

from app.domain.video import Video
from app.application.video_service import VideoService
from app.application.config_service import ConfigService
from app.application.video_metadata_service import VideoMetadataService


# ==================== Fixtures ====================

@pytest.fixture
def settings():
    return {
        "thumbnail_percent": 30,
        "application_path": "G:\\Git\\Dev\\OffTube",
    }


@pytest.fixture
def mock_video_service():
    svc = MagicMock(spec=VideoService)
    svc.get_all.return_value = []
    svc.clear_corrupted_videos.return_value = 0
    return svc


@pytest.fixture
def mock_config_service(settings):
    svc = MagicMock(spec=ConfigService)
    svc.get_setting.side_effect = settings.get
    return svc

@pytest.fixture
def video_metadata_service(mock_video_service, mock_config_service):
    return VideoMetadataService(mock_video_service, mock_config_service, "tests\\files")


# ==================== Tests ====================

def test_generate_thumbnail(video_metadata_service, mock_video_service):
    video = MagicMock(spec=Video)

    video.id = "1"
    video.filename = "video.mp4"
    video.path = "G:\\Git\\Dev\\OffTube\\tests\\files\\video.mp4"
    video.thumbnail = None
    video.duration = 1.234

    mock_video_service.get_video.return_value = video

    result, generated = video_metadata_service.fetch_thumbnail("abc")

    assert result == "video.mp4.jpg"
    assert generated is True
    mock_video_service.update_video.assert_called_with(video)


def test_fetch_thumbnail_returns_existing(video_metadata_service, mock_video_service):
    video = MagicMock(spec=Video)
    video.thumbnail = "existing.jpg"
    mock_video_service.get_video.return_value = video

    result, generated = video_metadata_service.fetch_thumbnail("abc")

    assert result == "existing.jpg"
    assert generated is False
    mock_video_service.update_video.assert_not_called()


def test_fetch_thumbnail_video_not_found(video_metadata_service, mock_video_service):
    mock_video_service.get_video.return_value = None

    result, generated = video_metadata_service.fetch_thumbnail("abc")

    assert result is None
    assert generated is False


def test_fetch_duration_returns_existing(video_metadata_service, mock_video_service):
    """Если duration уже есть — не генерируем."""
    video = MagicMock(spec=Video)
    video.duration = 123.4
    mock_video_service.get_video.return_value = video

    result, generated = video_metadata_service.fetch_duration("abc")

    assert result == 123.4
    assert generated is False