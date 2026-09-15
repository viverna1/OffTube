# video_importer.py
import os
import re
import logging

from app.domain.video import Video
from app.utils import generate_id, get_file_name
from app.application.video_service import VideoService
from app.application.config_service import ConfigService

log = logging.getLogger(__name__)



class VideoImporter:
    def __init__(self, video_service: VideoService, config_service: ConfigService, thumbnails_path: str, video_id_pattern: str) -> None:
        self._video_service = video_service
        self._config_service = config_service
        self._thumbnails_path = thumbnails_path
        self._video_id_pattern = video_id_pattern

    def sync_videos(self) -> list[Video]:
        existing_videos = self._video_service.get_all()
        existing_paths = {video.path for video in existing_videos.values()}

        videos = self._scan_videos(existing_paths)

        self._video_service.add_videos(videos)

        corrupted_count = self._video_service.clear_corrupted_videos()
        videos_after_cleanup = len(self._video_service.get_all())

        log.info("videos loaded: %s (%s new) (%s corrupted removed)", videos_after_cleanup, videos_after_cleanup - len(existing_videos), corrupted_count)

        return videos


    def _scan_videos(self, existing_paths: set[str]) -> list[Video]:
        video_extensions = self._config_service.get_setting("video_extensions")
        video_directories = self._config_service.get_setting("video_directories")
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
                        video = self._create_video_entry(root, filename)
                        videos.append(video)
        return videos

    # ? немного про нейминг. Такого рода методы называются mapper
    # ? convert_url_to_video
    # ? convert_url_to_domain (домен в данном случае означает, доменную сущность, то есть объект с которым работает твое приложение)
    # ? ещё их можно пихать в конструктор самого класса Video
    # и для этого нужен отдельный класс?
    # ? нет, класс не нужен. Названия обычно выглядят так
    # ? а вообще весь этот модуль - это слой infrastructure, так как он общается с внешней системой, в данном случае папками проекта

    def _create_video_entry(self, root: str, filename: str) -> Video:
        return Video(
            id=self._get_video_id(filename),
            name=get_file_name(filename),
            filename=filename,
            path=os.path.join(root, filename),
            thumbnail=self._find_existing_thumbnail(filename),
            duration=None
        )

    def _get_video_id(self, filename: str) -> str:
        match = re.search(self._video_id_pattern, filename)
        if match:
            return match.group(1)
        return generate_id()


    def _find_existing_thumbnail(self, video_filename: str) -> str | None:
        thumbnails_path = os.path.join(self._config_service.get_setting("application_path"), self._thumbnails_path)

        thumbnail_name = video_filename + ".jpg"
        thumbnail_path = os.path.join(thumbnails_path, thumbnail_name)

        if os.path.exists(thumbnail_path):
            return thumbnail_name
        return None
