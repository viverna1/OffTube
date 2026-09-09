# app.__init__.py
from flask import Flask

# ==================== CONSTS ====================
VIDEOS_CACHE_PATH = 'data/videos.json'
CONFIG_PATH = 'data/config.json'

# ==================== INFRASTRUCTURE ====================
from app.infrastructure.file_storage import FileStorage
from app.infrastructure.cache_storage import CacheStorage
from app.infrastructure.video_cache import VideoCache
from app.infrastructure.config_storage import ConfigStorage

cacheStorage = CacheStorage(VIDEOS_CACHE_PATH)
videoCache = VideoCache(cacheStorage)

configFileStorage = FileStorage(CONFIG_PATH)
configStorage = ConfigStorage(configFileStorage)

# ==================== APPLICATION ====================
from app.application.video_service import VideoService
from app.application.config_service import ConfigService

videoService = VideoService(videoCache)
configService = ConfigService(configStorage)

# ==================== PRESENTATION ====================
# from app.presentation.pages import pages_bp
# from app.presentation.api import api_bp
# from app.presentation.files import files_bp
# from app.presentation.admin import admin_bp


def create_app():
    configService.fix_application_path()
    # video_importer.sync_videos()

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="../static"
    )

    # app.register_blueprint(pages_bp)
    # app.register_blueprint(api_bp)
    # app.register_blueprint(files_bp)
    # app.register_blueprint(admin_bp)

    return app