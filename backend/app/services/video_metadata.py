# video_metadata.py
import os
import ffmpeg
import logging
from typing import Callable, Any

from app.data import Config, Videos

log = logging.getLogger(__name__)


def _generate_metadata(video_id: str, field: str, generator_func: Callable) -> tuple[Any, bool]:
    video_state = Videos.get_video(video_id)

    if not video_state: return None, False
    if video_state[field]: return video_state[field], False

    result = generator_func(video_state)

    if result is None:
        log.error(f"Failed to fetch {field} for video: %s", video_state["id"])
        return None, False

    video_state[field] = result
    Videos.update_video(video_state)

    return video_state[field], True


def fetch_thumbnail(video_id: str) -> tuple[str | None, bool]:
    return _generate_metadata(video_id, "thumbnail", _generate_thumbnail)


def fetch_duration(video_id: str) -> tuple[float | None, bool]:
    return _generate_metadata(video_id, "duration", _get_video_duration)


def _generate_thumbnail(video_state: dict) -> str | None:
    duration = fetch_duration(video_state["id"])[0]

    if duration is None:
        return None

    percent = Config.get_setting("thumbnail_percent")
    time_str = _calculate_percentile_time(duration, percent)
    
    thumbnails_path = Config.get_setting("thumbnails_path")
    output_path = os.path.join(thumbnails_path, video_state["filename"] + '.jpg')
    
    log.debug("generate thumbnail for: %s", video_state["id"])

    # Извлекаем кадр
    (
        ffmpeg
        .input(video_state["path"], ss=time_str)
        .output(output_path, vframes=1)
        .run(overwrite_output=True, quiet=True)
    )
    
    thumbnail = os.path.basename(output_path)
    return thumbnail


def _get_video_duration(video_state: dict) -> float:
    log.debug("generate duration for: %s", video_state["id"])

    probe = ffmpeg.probe(video_state["path"])
    duration = float(probe['format']['duration'])

    return duration


def _calculate_percentile_time(time: float, percent: float) -> str:
    time_seconds = time * (percent / 100)
    
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

