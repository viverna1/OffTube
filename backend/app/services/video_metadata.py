# video_metadata.py
import os
import ffmpeg
import logging

from app.data import Config, Videos

log = logging.getLogger(__name__)


def _generate_metadata(video_id, field, generator_func):
    video_state = Videos.get_video(video_id)

    if not video_state: return None, False
    if video_state[field]: return video_state[field], False

    video_state[field] = generator_func(video_state)
    Videos.update_video(video_state)

    return video_state[field], True


def _generate_thumbnail(video_state):
    duration = fetch_duration(video_state["id"])[0]

    percent = Config.get_setting("thumbnail_percent")

    time_str = _calculate_percentile_time(duration, percent)
    
    output_path = Config.get_setting("thumbnails_path")
    output_path = os.path.join(output_path, video_state["filename"] + '.jpg')
    
    log.debug("generate thumbnail for: %s", video_state["id"])

    # Извлекаем кадр
    (
        ffmpeg
        .input(video_state["path"], ss=time_str)
        .output(output_path, vframes=1)
        .run(overwrite_output=True, quiet=True)
    )
    
    return output_path


def fetch_thumbnail(video_id: str) -> tuple[str | None, bool]:
    video_state = Videos.get_video(video_id)

    if not video_state:
        return None, False


    if video_state["thumbnail"]:
        return (video_state["thumbnail"], False)

    thumbnail_path = _generate_thumbnail(video_state)
    thumbnail = os.path.basename(thumbnail_path)

    video_state["thumbnail"] = thumbnail
    Videos.update_video(video_state)

    return (thumbnail, True)


def _calculate_percentile_time(time, percent):
    time_seconds = time * (percent / 100)
    
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# ==================== Duration ====================
def _get_video_duration(video_state: dict) -> float:
    log.debug("generate duration for: %s", video_state["id"])

    probe = ffmpeg.probe(video_state["path"])
    duration = float(probe['format']['duration'])

    return duration


def fetch_duration(video_id) -> tuple[float | None, bool]:
    video_state = Videos.get_video(video_id)

    if not video_state:
        return None, False

    if video_state["duration"] is not None:
        return video_state["duration"], False

    duration = _get_video_duration(video_state)

    video_state["duration"] = duration
    Videos.update_video(video_state)

    return duration, True
