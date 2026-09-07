# videos_cache.py
import logging

from app.domain.video import Video
from app.infrastructure.base_cache import BaseCache

log = logging.getLogger(__name__)

VIDEOS_CACHE_PATH = 'data/videos.json'


class VideosCache(BaseCache):
    # getters
    def get_all_videos(self) -> dict[str, Video]:
        return {key: Video.from_dict(video) for key, video in super().get_all().items()}

    def get_by_id(self, video_id: str) -> Video | None:
        video = super().get(video_id)
        if video is None:
            return None
        return Video.from_dict(video)
    
    # setters
    def set_video(self, video: Video) -> None:
        self.set(video.id, video.to_dict())

    def add_videos(self, videos: dict[str, Video]) -> None:
        added_videos = {video_id: video.to_dict() for video_id, video in videos.items()}
        self.set_batch(added_videos)

videoCache = VideosCache(VIDEOS_CACHE_PATH)