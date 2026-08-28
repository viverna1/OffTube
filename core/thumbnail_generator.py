# thumbnail_generator.py
import os
import ffmpeg

import core.file_manager as file_manager
from core.data import Videos, Config


def fetch_thumbnail(video_id: str) -> tuple[str | None, bool]:
    video_state = Videos.get_video(video_id)

    if not video_state:
        return None, False

    if video_state["thumbnail"]:
        return (video_state["thumbnail"], False)

    thumbnail = _generate_thumbnail(video_state)
    video_state["thumbnail"] = thumbnail
    Videos.update_video(video_state)

    return (thumbnail, True)



def _generate_thumbnail(video_state):

    duration = file_manager.fetch_duration(video_state["id"])[0]

    percent = Config.get_setting("thumbnail_percent")

    time_str = _calculate_percentile_time(duration, percent)
    
    output_path = Config.get_setting("thumbnails_path")
    output_path = os.path.join(output_path, video_state["filename"] + '.jpg')
    
    print("generate thumbnail for:", video_state["id"])

    # Извлекаем кадр
    (
        ffmpeg
        .input(video_state["path"], ss=time_str)
        .output(output_path, vframes=1)
        .run(overwrite_output=True, quiet=True)
    )
    
    return output_path


def _calculate_percentile_time(time, percent):
    time_seconds = time * (percent / 100)
    
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
