# test_videos_cache.py
import unittest
from unittest.mock import patch

from app.domain.video import Video
from app.infrastructure.videos_cache import VideosCache


def create_video(number: str):
    return Video(
        id=number,
        name=f"vid{number}",
        filename=f"vid{number}.mp4",
        path=f"vids/vid{number}.mp4",
        thumbnail=f"thumb/vid{number}.mp4.jpg",
        duration=1.5
    )


class TestVideosCache(unittest.TestCase):
    def setUp(self):
        self.load_patcher = patch.object(VideosCache, 'load', return_value={})
        self.save_patcher = patch.object(VideosCache, 'save')
        self.mock_load = self.load_patcher.start()
        self.mock_save = self.save_patcher.start()

        self.videosCache = VideosCache("test_cache.json")

    def tearDown(self):
        self.load_patcher.stop()
        self.save_patcher.stop()


    def test_set_and_get(self):
        video = create_video("1")
        self.videosCache.set_video(video)
        self.assertEqual(self.videosCache.get_by_id("1"), video)
        self.mock_save.assert_called_once()

    def test_add_videos(self):
        video1 = create_video("1")
        video2 = create_video("2")
        self.videosCache.add_videos({video1.id: video1, video2.id: video2})
        self.assertEqual(self.videosCache.get_by_id(video1.id), video1)
        self.assertEqual(self.videosCache.get_by_id(video2.id), video2)
        self.mock_save.assert_called()

    def test_delete(self):
        video = create_video("2")
        self.videosCache.set_video(video)
        self.videosCache.delete("2")
        self.assertIsNone(self.videosCache.get_by_id("2"))
        self.mock_save.assert_called()

    def test_invalid_id(self):
        self.assertEqual(self.videosCache.get_by_id("1"), None)

    def test_delete_nonexistent(self):
        self.videosCache.delete("999")
        self.mock_save.assert_not_called()
