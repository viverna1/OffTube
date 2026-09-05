# app.__init__.py
from flask import Flask

from app.services.video_importer import import_all_videos


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    import_all_videos()

    from app.routes import pages_bp, files_bp, api_bp, admin_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    return app