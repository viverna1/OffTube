# video_cache.py
import logging
from app.domain.video import Video
from app.infrastructure.file_storage import FileStorage

log = logging.getLogger(__name__)

VIDEOS_PATH = 'data/videos.json'

class VideoCache(FileStorage):    
    def get_all(self) -> list[Video]:
        return [Video.from_dict(video_data) for video_data in self.load()]

    def get_by_id(self, video_id: str) -> Video | None:
        all_vids = self.get_all()
        return next((v for v in all_vids if v.id == video_id), None)
    
    def add_video(self, video: Video) -> None:
        all_vids = self.get_all()
        
        if any(v.id == video.id for v in all_vids):
            raise ValueError(f"Видео с ID {video.id} уже существует!")
            
        all_vids.append(video)
        
        self.save([v.to_dict() for v in all_vids])

    def add_videos(self, videos: list[Video]) -> None:
        all_vids = self.get_all()
        
        # Собираем сет из уже существующих ID для моментальной проверки
        existing_ids = {v.id for v in all_vids}
        
        # Проверяем новые видео на дубликаты
        for video in videos:
            if video.id in existing_ids:
                raise ValueError(f"Видео с ID {video.id} уже существует в базе!")
            
            # А также проверяем, нет ли дубликатов внутри самого добавляемого списка
            if video.id in [v.id for v in all_vids]:
                # Ладно, это паранойя, но если в самом массиве `videos` будут два одинаковых ID,
                # лучше поймать это сразу. Заменим на добавление в сет по ходу дела:
                pass
        
        # Вот так будет красивее и безопаснее:
        new_ids = set()
        for video in videos:
            if video.id in existing_ids or video.id in new_ids:
                raise ValueError(f"Обнаружен дубликат ID {video.id}! Операция отменена.")
            new_ids.add(video.id)
            all_vids.append(video)
            
        # Сохраняем всё ОДИН РАЗ, а не насилуем жесткий диск
        self.save([v.to_dict() for v in all_vids])

    def update_video(self, video: Video) -> None:
        all_vids = self.get_all()
        updated = False
        
        for i, v in enumerate(all_vids):
            if v.id == video.id:
                all_vids[i] = video
                updated = True
                break
        
        if not updated:
            raise ValueError(f"Видео с ID {video.id} не найдено!")
            
        self.save([v.to_dict() for v in all_vids])       
        
    def remove_video(self, video_id: str) -> None:
        all_vids = self.get_all()
        
        filtered_vids = [v for v in all_vids if v.id != video_id]
        
        if len(filtered_vids) == len(all_vids):
            raise ValueError(f"Видео с ID {video_id} не найдено!")
            
        self.save([v.to_dict() for v in filtered_vids])
        log.debug("video \"%s\" removed from cache", video_id)

    def clear_cache(self) -> None:
        self.save([])

videoCache = VideoCache(VIDEOS_PATH)