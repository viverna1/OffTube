# videos_data.py
from .base_storage import Storage
import core.video_importer as video_importer

VIDEOS_PATH = 'data/videos.json'


class VideoStorage(Storage):
    def __init__(self, filepath):
        super().__init__(filepath)
        self._data = video_importer.import_all_videos()

    def _init_empty(self):
        self._data = []

    def get_videos(self, start_index: int, count: int):
        if start_index >= len(self._data):
            return []
        
        end_index = start_index + count
        result = self._data[start_index:end_index]

        return result
    
    def get_video(self, video_id):
        for video in self._data:
            if video["id"] == video_id:
                return video

    def get_video_by_path(self, video_path):
        for video in self._data:
            if video["path"] == video_path:
                return video
            
    def update_video(self, video_state):
        for i, video in enumerate(self._data):
            if video['id'] == video_state['id']:
                self._data[i] = video_state
                break


Videos = VideoStorage(VIDEOS_PATH)
