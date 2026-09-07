from app.infrastructure.video_cache2 import VideoCache
from app.infrastructure.base_cache import BaseCache


# class FileStorageMock(FileStorage):
#     def load(self):
#         return [
#             {
#                 "id": "1",
#                 "name": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA",
#                 "filename": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4",
#                 "path": "C:\\Users\\viverna\\Desktop\\OffTube\\vids\\5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4",
#                 "thumbnail": "5G4iyqfIyJRNTvBpHOUa+AdVy5xtY4bA.mp4.jpg",
#                 "duration": null
#             },
#             {
#                 "id": "2",
#                 "name": "vid",
#                 "filename": "vid.mp4",
#                 "path": "C:\\Users\\viverna\\Desktop\\OffTube\\vids\\vid.mp4",
#                 "thumbnail": "vid.mp4.jpg",
#                 "duration": null
#             },
#             {
#                 "id": "HUF-jWGPNHI",
#                 "name": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI]",
#                 "filename": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv",
#                 "path": "C:\\Users\\viverna\\Desktop\\OffTube\\vids\\What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv",
#                 "thumbnail": "What is the FASTEST way to TUNNEL in Minecraft [HUF-jWGPNHI].mkv.jpg",
#                 "duration": null
#             }
#         ]

#     def save(self, val):
#         print("save:", val)


baseCache = BaseCache("videos.json")
print(baseCache.exists())
print(baseCache.get("2"))

baseCache.set("3", "123")
print(baseCache.get("3"))
print(baseCache.has("3"))
baseCache.delete("3")
print(baseCache.has("3"))

baseCache.set_batch({"4": "12333", "5": "12344"})
print(baseCache.get("4"))
print(baseCache.has("5"))

baseCache.delete("4")
baseCache.delete("5")

print(baseCache.has("5"))


# videoCache = VideoCache("videos.json")
# print(videoCache.get("2"))