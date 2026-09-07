# video_metadata.py
import os
import ffmpeg
import logging
from typing import Callable, Any

from app.domain.video import Video
from app.utils import formate_time
from app.application.video_service import videoService
from app.application.config_service import configService

log = logging.getLogger(__name__)

THUMBIAILS_PATH = "backend\\static\\thumbnails"


def _generate_metadata(video_id: str, field: str, generator_func: Callable) -> tuple[Any, bool]:
    video = videoService.get_video(video_id)

    if not video: return None, False
    if getattr(video, field): return getattr(video, field), False

    result = generator_func(video)

    if result is None:
        log.error("Failed to fetch %s for video: %s", field, video.id)
        return None, False

    setattr(video, field, result)
    videoService.update_video(video)

    return getattr(video, field), True


def fetch_thumbnail(video_id: str) -> tuple[str | None, bool]:
    return _generate_metadata(video_id, "thumbnail", _generate_thumbnail)


def fetch_duration(video_id: str) -> tuple[float | None, bool]:
    return _generate_metadata(video_id, "duration", _generate_video_duration)


def _generate_thumbnail(video: Video) -> str | None:
    duration = fetch_duration(video.id)[0]

    if duration is None:
        return None

    percent = configService.get_setting("thumbnail_percent")
    time_str = formate_time(duration * (percent / 100))

    thumbnails_path = os.path.join(configService.get_setting("application_path"), THUMBIAILS_PATH)
    output_path = os.path.join(thumbnails_path, video.filename + '.jpg')

    log.debug("generate thumbnail for id: %s, frame time: %s", video.name, time_str)

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


def _generate_video_duration(video: Video) -> float | None:
    log.debug("generate duration for: %s", video.name)

    try:
        probe = ffmpeg.probe(video.path)
        duration = float(probe['format']['duration'])

        return duration
    except AttributeError:
        log.error("ffmpeg not installed")
        return None
