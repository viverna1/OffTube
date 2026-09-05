# videos_storage.py
from .base_storage import Storage
import logging

log = logging.getLogger(__name__)

VIDEOS_PATH = 'data/videos.json'


class VideoStorage(Storage):
    def get_videos(self, offset: int, limit: int):
        if offset >= len(self._data):
            return []
        
        end_index = offset + limit
        result = self._data[offset:end_index]

        log.debug(f"getting videos with offset={offset}, limit={limit}. Returning {len(result)} videos.")
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
        self.save()

    def add_video(self, video_state):
        if self.get_video(video_state['id']) is not None:
            return
        self._data.append(video_state)
        self.save()

    def clear_cache(self):
        self._data = []
        self.save()


Videos = VideoStorage(VIDEOS_PATH)
