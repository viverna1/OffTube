# test_video_importer.py
import pytest
from unittest.mock import MagicMock

from app.application.video_service import VideoService
from app.application.config_service import ConfigService
from app.infrastructure.video_importer import VideoImporter

#мяв

# ==================== Fixtures ====================

@pytest.fixture
def settings():
    return {
        "video_extensions": [".mp4", ".mkv"],
        "video_directories": [],
        "application_path": "",
    }


@pytest.fixture
def mock_video_service():
    svc = MagicMock(spec=VideoService)
    svc.get_all.return_value = {}
    svc.clear_corrupted_videos.return_value = 0
    return svc


@pytest.fixture
def mock_config_service(settings):
    svc = MagicMock(spec=ConfigService)
    svc.get_setting.side_effect = settings.get
    return svc


@pytest.fixture
def video_importer(mock_video_service, mock_config_service):
    return VideoImporter(
        video_service=mock_video_service,
        config_service=mock_config_service,
        thumbnails_path="thumbnails",
        video_id_pattern=r"\[([\w-]+)\]",
    )


# ==================== Tests ====================

def test_sync_videos_collects_new_files(video_importer, mock_video_service, settings, tmp_path):
    vids = tmp_path / "vids"
    vids.mkdir()
    (vids / "alpha [id1].mp4").write_bytes(b"")
    (vids / "beta.mkv").write_bytes(b"")
    (vids / "readme.txt").write_text("ignore me")

    settings["video_directories"] = [str(vids)]

    result = video_importer.sync_videos()

    assert {v.filename for v in result} == {"alpha [id1].mp4", "beta.mkv"}
    assert any(v.id == "id1" for v in result)

    mock_video_service.add_videos.assert_called_once()
    added = mock_video_service.add_videos.call_args.args[0]
    assert len(added) == 2

    mock_video_service.clear_corrupted_videos.assert_called_once()
    