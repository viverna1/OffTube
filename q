# file_manager_old
import os
import json
import re
import ffmpeg

VIDEO_ID_PATTERN = r'\[(.*?)\]'
SETTINGS_PATH = 'static/settings.json'
VIDEOS_PATH = 'static/videos.json'

def find_video(video_id):
    with open(VIDEOS_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)
        for video in videos:
            if video['id'] == video_id:
                return video
    return None

def get_all_videos():
    if os.path.exists(VIDEOS_PATH):
        videos_mtime = os.path.getmtime(VIDEOS_PATH)
        with open(SETTINGS_PATH) as f:
            config = json.load(f)
        latest_mtime = videos_mtime
        for directory in config.get('video_directories', []):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.mp4', '.mkv', '.avi')):
                        mtime = os.path.getmtime(os.path.join(root, file))
                        if mtime > latest_mtime:
                            latest_mtime = mtime
                            
        if videos_mtime >= latest_mtime:
            with open(VIDEOS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)

    videos = _scan_videos()
    with open(VIDEOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos, f)
    return videos


def _scan_videos():
    videos = []
    with open(SETTINGS_PATH) as f:
        config = json.load(f)
        video_directories = config.get('video_directories', [])

    for directory in video_directories:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(('.mp4', '.mkv', '.avi')):

                    video_id = _get_video_id_from_filename(filename)
                    name = _get_video_name_from_filename(filename)
                    path = os.path.join(root, filename)
                    thumbnail = _get_video_thumbnail_name(os.path.join(directory, filename))

                    videos.append({
                        'id': video_id,
                        'name': name,
                        'filename': filename,
                        'path': path,
                        'thumbnail': thumbnail,
                        'duration': None
                    })
    
    # videos = [
    #     {'id': 'XYb4zclX5-U','name': 'Video 1', 'filename': 'ВОТ ПОЧЕМУ НЕ СТОИТ СТРОИТЬ ТЫСЯЧИ АЭРОПОРТОВ ｜ PLAGUE INC [XYb4zclX5-U].mkv', 'thumbnail': 'placeholder.png'},
    #     {'id': None, 'name': 'Video 2', 'filename': 'vid.mkv', 'thumbnail': None},
    #     {'id': 'wertt','name': 'Video 3', 'filename': 'video3.mkv', 'thumbnail': None},
    # ]

    return videos

def _get_video_id_from_filename(filename):
    match = re.search(VIDEO_ID_PATTERN, filename)
    if match:
        return match.group(1)

def _get_video_name_from_filename(filename):
    name = re.sub(VIDEO_ID_PATTERN, '', filename)
    name = os.path.splitext(name)[0]
    return name.strip()

def generate_thumbnail(video_path, output_path=None, percent=30):
    if not output_path:
        with open(SETTINGS_PATH) as f:
            config = json.load(f)
            output_path = config.get('thumbnails_path', [])

    duration = get_video_duration(video_path)
    time_str = _calculate_percentile_time(duration, percent)
    
    output_path = os.path.join(
        output_path, 
        os.path.splitext(os.path.basename(video_path))[0] + '.jpg'
    )
    
    # Извлекаем кадр
    (
        ffmpeg
        .input(video_path, ss=time_str)
        .output(output_path, vframes=1)
        .run(overwrite_output=True, quiet=True)
    )
    
    return output_path

def _calculate_percentile_time(duration, percent):
    time_seconds = duration * (percent / 100)
    
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    seconds = int(time_seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def _get_video_thumbnail_name(video_path):
    with open(SETTINGS_PATH) as f:
        config = json.load(f)
        thumbnails_path = config.get('thumbnails_path', [])

    for file in os.listdir(thumbnails_path):
        if _get_file_name(video_path) == _get_file_name(file):
            return file
    return None

def _get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def get_video_duration(video_path):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    return duration
