# video_importer.py
import os
import re
import logging

from app.domain.video import Video
from app.utils import next_id, get_file_name
from app.application.video_service import videoService
from app.application.config_service import configService

log = logging.getLogger(__name__)

VIDEO_ID_PATTERN = r'\[(.*?)\]'
THUMBIAILS_PATH = "backend\\static\\thumbnails"


def sync_videos() -> list[Video]:
    existing_videos = videoService.get_all()
    existing_paths = {video.path for video in existing_videos}

    videos = _scan_videos(existing_paths)

    videoService.add_videos(videos)

    corrupted_count = videoService.clear_corrupted_videos()
    videos_after_cleanup = len(videoService.get_all())

    log.info("videos loaded: %s (%s new) (%s corrupted removed)", videos_after_cleanup, len(existing_videos) - videos_after_cleanup, corrupted_count)

    return videos


def _scan_videos(existing_paths: set[str]) -> list[Video]:
    video_extensions = configService.get_setting("video_extensions")
    video_directories = configService.get_setting("video_directories")
    videos = []

    for directory in video_directories:
        if not os.path.exists(directory):
            log.warning(f"Path {directory} not found")
            continue

        for root, _, files in os.walk(directory):
            for filename in files:

                file_path = os.path.join(root, filename)
                if file_path in existing_paths:
                    continue

                if filename.endswith(tuple(video_extensions)):
                    video = _create_video_entry(root, filename)
                    videos.append(video)
    return videos


def _create_video_entry(root: str, filename: str) -> Video:
    return Video(
        id=_get_video_id(filename),
        name=get_file_name(filename),
        filename=filename,
        path=os.path.join(root, filename),
        thumbnail=_find_existing_thumbnail(filename),
        duration=None
    )


def _get_video_id(filename: str) -> str:
    match = re.search(VIDEO_ID_PATTERN, filename)
    if match:
        return match.group(1)
    return next_id()


def _find_existing_thumbnail(video_filename: str) -> str | None:
    thumbnails_path = os.path.join(configService.get_setting("application_path"), THUMBIAILS_PATH)

    thumbnail_name = video_filename + ".jpg"
    thumbnail_path = os.path.join(thumbnails_path, thumbnail_name)

    if os.path.exists(thumbnail_path):
        return thumbnail_name
    return None


# !TODO: Переделать
class videoImporter():
    def sync_videos(self):
        return sync_videos()

video_importer = videoImporter()