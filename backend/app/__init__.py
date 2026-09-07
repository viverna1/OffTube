# app.__init__.py
from flask import Flask

from app.application import video_importer
from app.utils import validate_application_path

# from app.infrastructure.file_storage import FileStorage
# from app.infrastructure.video_cache import VideoCache

# base_storage = FileStorage("abs")
# video_cache = VideoCache(cache_storage)
# video_repository = VideoRepository()
# video_service = VideoService(video_repository, video_cache)


def create_app():
    validate_application_path()
    
    app = Flask(
        __name__,
        template_folder="presentation/ui/templates",
        static_folder="../static"
    )

    video_importer.sync_videos()

    from app.presentation.ui.pages import pages_bp
    from app.presentation.api import api_bp
    from app.presentation.files import files_bp
    from app.presentation.admin import admin_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)


    return app