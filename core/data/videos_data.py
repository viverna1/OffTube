# videos_data.py
from .base_storage import Storage

VIDEOS_PATH = 'data/videos.json'


class VideoStorage(Storage):
    def __init__(self, filepath):
        super().__init__(filepath)
        self._last_video_index = 0

    def _init_empty(self):
        self._data = []

    def set_data(self, data):
        self._data = data
        self.save()

    def get_videos(self, count: int):
        if self._last_video_index >= len(self._data):
            return []
        
        end_index = self._last_video_index + count
        result = self._data[self._last_video_index:end_index]

        self._last_video_index = end_index
        return result

    def reset_counter(self):
        self._last_video_index = 0
    
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
