# app.__init__.py
from flask import Flask

# ==================== CONSTS ====================
VIDEOS_CACHE_PATH = 'data/videos.json'
CONFIG_PATH = 'data/config.json'
THUMBNAILS_PATH = "static\\thumbnails"
VIDEO_ID_PATTERN = r'\[(.*?)\]'

# ==================== INFRASTRUCTURE ====================
from app.infrastructure.repository.json_repository import JsonRepository
from app.infrastructure.repository.cache_repository import CacheRepository
from app.infrastructure.repository.video_cache import VideoCache
from app.infrastructure.repository.config_repository import ConfigRepository
from app.infrastructure.video_importer import VideoImporter

cache_storage = CacheRepository(VIDEOS_CACHE_PATH)
video_cache = VideoCache(cache_storage)

config_json_repo = JsonRepository(CONFIG_PATH)
config_storage = ConfigRepository(config_json_repo)

# ==================== APPLICATION ====================
from app.application.video_service import VideoService
from app.application.config_service import ConfigService
from app.application.video_metadata_service import VideoMetadataService

video_service = VideoService(video_cache)
config_service = ConfigService(config_storage)
video_metadata_service = VideoMetadataService(video_service, config_service, THUMBNAILS_PATH)

# TODO VideoImporter принадлежит к INFRASTRUCTURE, передвинуть
video_importer = VideoImporter(video_service, config_service, THUMBNAILS_PATH, VIDEO_ID_PATTERN)

# ==================== App ====================
def create_app():
    config_service.fix_application_path()
    video_importer.sync_videos()

    app = Flask(
        __name__,
        template_folder="presentation/ui/templates",
        static_folder="../static"
    )

    # app.extensions['VIDEO_SERVICE'] = video_service
    # app.extensions['CONFIG_SERVICE'] = config_service

    # ==================== PRESENTATION ====================
    from app.presentation.ui.pages import pages_bp
    from app.presentation.api.video import api_bp
    from app.presentation.api.files import files_bp
    # from app.presentation.api.admin import admin_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(files_bp)
    # app.register_blueprint(admin_bp)

    return app