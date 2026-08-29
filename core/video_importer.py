# video_importer.py
import os
import re

from core.data.config_storage import Config
import core.utils as utils


VIDEO_ID_PATTERN = r'\[(.*?)\]'


def import_all_videos():
    videos = _scan_videos()
    return videos


def _scan_videos():
    video_extensions = tuple(Config.get_setting("video_extensions"))
    video_directories = Config.get_setting("video_directories")
    videos = []

    for directory in video_directories:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(video_extensions):
                    video = _create_video_entry(root, filename)
                    videos.append(video)
    return videos


def _create_video_entry(root, filename):
    return {
        'id': _get_video_id(filename),
        'name': _get_file_name(filename),
        'filename': filename,
        'path': os.path.join(root, filename),
        'thumbnail': _find_existing_thumbnail(filename),
        'duration': None
    }


def _get_video_id(filename: str) -> str:
    match = re.search(VIDEO_ID_PATTERN, filename)
    if match:
        return match.group(1)
    else:
        return utils.IdGenerator.get_id()


def _find_existing_thumbnail(video_filename: str) -> str | None:
    thumbnails_path = Config.get_setting("thumbnails_path")

    thumbnail_name = video_filename + ".jpg"
    thumbnail_path = os.path.join(thumbnails_path, thumbnail_name)

    if os.path.exists(thumbnail_path):
        return thumbnail_name
    return None


def _get_file_name(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]
