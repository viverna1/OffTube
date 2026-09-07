# test_base_cache.py
import unittest
from typing import Any

from app.infrastructure.base_cache import BaseCache


class BaseCacheMock(BaseCache):
    def __init__(self):
        self._storage = {}
        self.filepath = ""

    def save(self) -> Any:
        return
        print("save!")

    def load(self) -> dict:
        return {
            "1": {
                "id": "1",
                "name": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA",
                "filename": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4",
                "path": "G:\\Git\\Dev\\OffTube\\vids\\5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4",
                "thumbnail": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4.jpg",
                "duration": 167.137234
            },
            "2": {
                "id": "2",
                "name": "vid",
                "filename": "vid.mp4",
                "path": "G:\\Git\\Dev\\OffTube\\vids\\vid.mp4",
                "thumbnail": "vid.mp4.jpg",
                "duration": 152.322902
            },
            "HUF-jWGPNHI": {
                "id": "HUF-jWGPNHI",
                "name": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI]",
                "filename": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv",
                "path": "G:\\Git\\Dev\\OffTube\\vids\\What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv",
                "thumbnail": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv.jpg",
                "duration": 469.528
            }
        }

class TestBaseCache(unittest.TestCase):
    def setUp(self):
        self.baseCache = BaseCacheMock()

    def test_get_set(self):
        self.baseCache.set("key", "value")
        self.assertEqual(self.baseCache.get("key"), "value")

    def test_delete(self):
        self.baseCache.set("key", "value")
        self.baseCache.delete("key")
        self.assertFalse(self.baseCache.has("key"))

    def test_set_batch(self):
        self.baseCache.set_batch({"key1": "value1", "key2": "value2"})
        self.assertEqual(self.baseCache.get("key1"), "value1")
        self.assertEqual(self.baseCache.get("key2"), "value2")
        