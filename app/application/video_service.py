# video_service.py
import logging

from app.domain.video import Video
from app.infrastructure.video_cache import VideoCache, videoCache

log = logging.getLogger(__name__)

class VideoService:
    def __init__(self, cache: VideoCache) -> None:
        self._cache = cache
    
    # getters
    def get_all(self) -> list[Video]:
        return self._cache.get_all()    
    
    def get_video(self, video_id: str) -> Video | None:
        video_dict = self._cache.get_by_id(video_id)
        if video_dict is None:
            return None

        if not video_dict.exists():
            log.warning("video %s does not exist, removing", video_dict.path)
            self._cache.remove_video(video_dict.id)
            return None

        return video_dict

    def get_banch_videos(self, offset: int, limit: int) -> list[Video]:
        all_videos = self._cache.get_all()
        result = []
        index = offset

        while len(result) < limit and index < len(all_videos):
            video_dict = all_videos[index]
            if video_dict.exists():
                result.append(video_dict)
            index += 1

        log.debug(f"getting videos with offset={offset}, limit={limit}. Returning {len(result)} videos.")
        return result

    def update_video(self, video: Video):
        return self._cache.update_video(video)

    def add_videos(self, videos: list[Video]):
        return self._cache.add_videos(videos)

    # mutators
    def clear_corrupted_videos(self) -> int:
        all_videos = self._cache.get_all()
        corrupted = [v for v in all_videos if not v.exists()]

        for video in corrupted:
            log.warning("video %s does not exist, and was removed", video.path)
            self._cache.remove_video(video.id)

        return len(corrupted)
    
    def clear_cache(self):
        self._cache.clear_cache()
    
videoService = VideoService(videoCache)