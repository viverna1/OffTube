# video_cache.py
import logging

from app.domain.video import Video
from app.infrastructure.cache_storage import CacheStorage

log = logging.getLogger(__name__)


class VideoCache():
    def __init__(self, cache: CacheStorage):
        self._cache: CacheStorage = cache

    # getters
    def get_all(self) -> dict[str, Video]:
        return {key: Video.from_dict(video) for key, video in self._cache.get_all().items()}

    def get_by_id(self, video_id: str) -> Video | None:
        video = self._cache.get(video_id)
        if video is None:
            return None
        return Video.from_dict(video)
    
    # setters
    def set_video(self, video: Video) -> None:
        self._cache.set(video.id, video.to_dict())

    def add_videos(self, videos: list[Video]) -> None:
        added_videos = {video.id: video.to_dict() for video in videos}
        self._cache.set_batch(added_videos)

    def delete(self, video_id: str) -> None:
        self._cache.delete(video_id)

    def clear_cache(self,) -> None:
        self._cache.clear_cache()

# VIDEOS_CACHE_PATH = 'data/videos.json'
# videoCache = VideoCache(VIDEOS_CACHE_PATH)