# video_metadata.py
import os
import ffmpeg
import logging
from typing import Callable, Any

from app.domain.video import Video
from app.application.video_service import VideoService
from app.application.config_service import ConfigService
from app.utils.time_utils import formate_time

log = logging.getLogger(__name__)


class VideoMetadataService:
    def __init__(self, video_service: VideoService, config_service: ConfigService, thumbnails_path: str) -> None:
        self._video_service = video_service
        self._config_service = config_service
        self._thumbnails_path = thumbnails_path

    # Public
    def fetch_thumbnail(self, video_id: str) -> tuple[str | None, bool]:
        return self._generate_metadata(video_id, "thumbnail", self._generate_thumbnail)


    def fetch_duration(self, video_id: str) -> tuple[float | None, bool]:
        return self._generate_metadata(video_id, "duration", self._generate_video_duration)

    # Private
    def _generate_metadata(self, video_id: str, field: str, generator_func: Callable) -> tuple[Any, bool]:
        video = self._video_service.get_video(video_id)

        if not video: return None, False
        if getattr(video, field): return getattr(video, field), False

        result = generator_func(video)

        if result is None:
            log.error("Failed to fetch %s for video: %s", field, video.id)
            return None, False

        setattr(video, field, result)
        self._video_service.update_video(video)

        return getattr(video, field), True


    def _generate_thumbnail(self, video: Video) -> str | None:
        duration = self.fetch_duration(video.id)[0]

        if duration is None:
            return None

        percent = self._config_service.get_setting("thumbnail_percent")
        time_str = formate_time(duration * (percent / 100))

        thumbnails_path = os.path.join(self._config_service.get_setting("application_path"), self._thumbnails_path)
        output_path = os.path.join(thumbnails_path, video.filename + '.jpg')

        log.debug("generate thumbnail for id: %s, frame time: %s", video.filename, time_str)

        try:
            (
                ffmpeg
                .input(video.path, ss=time_str)
                .output(output_path, vframes=1)
                .run(overwrite_output=True, quiet=True)
            )

            thumbnail = os.path.basename(output_path)
            return thumbnail
        except AttributeError:
            log.error("ffmpeg not installed")
            return None


    def _generate_video_duration(self, video: Video) -> float | None:
        log.debug("generate duration for: %s", video.name)

        try:
            probe = ffmpeg.probe(video.path)
            duration = float(probe['format']['duration'])

            return duration
        except AttributeError:
            log.error("ffmpeg not installed")
            return None
