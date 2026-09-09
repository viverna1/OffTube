# video_service.py
import logging

from app.domain.video import Video
from app.infrastructure.video_cache import VideoCache

log = logging.getLogger(__name__)


class VideoService:
    def __init__(self, cache: VideoCache) -> None:
        self._cache = cache
    
    # getters
    def get_video(self, video_id: str) -> Video | None:
        video = self._cache.get_by_id(video_id)
        if video is None:
            return None

        if not video.exists():
            log.warning("video %s does not exist, removing", video.path)
            self._cache.delete(video.id)
            return None

        return video

    def get_batch_videos(self, offset: int, limit: int) -> list[Video]:
        all_videos = list(self._cache.get_all().values())
        result = all_videos[offset:offset + limit]
        log.debug(f"getting videos with offset={offset}, limit={limit}. Returning {len(result)} videos.")
        return result
    
    # def get_batch_videos2(self, offset: int, limit: int) -> list[Video]:
    #     all_videos: list[Video] = self._cache.get_all().keys()
    #     c = all_videos
    #     result = []
    #     index = offset

    #     while len(result) < limit and index < len(all_videos):
    #         video_dict = all_videos[index]
    #         if video_dict.exists():
    #             result.append(video_dict)
    #         index += 1

    #     log.debug(f"getting videos with offset={offset}, limit={limit}. Returning {len(result)} videos.")
    #     return result

    def add_video(self, video: Video):
        self._cache.set_video(video)

    def update_video(self, video: Video):
        self._cache.set_video(video)

    def add_videos(self, videos: list[Video]):
        self._cache.add_videos(videos)

    def delete(self, video_id: str) -> None:
        self._cache.delete(video_id)

    # mutators
    def clear_corrupted_videos(self) -> int:
        all_videos = self._cache.get_all()
        corrupted = [v for v in all_videos.values() if not v.exists()]

        for video in corrupted:
            log.warning("video %s does not exist, and was removed", video.path)
            self._cache.delete(video.id)

        return len(corrupted)
    
    def clear_cache(self):
        self._cache.clear_cache()
