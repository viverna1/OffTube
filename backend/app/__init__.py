from flask import Flask

from app.services.video_importer import import_all_videos


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    import_all_videos()

    from app.routes import register_routes
    register_routes(app)
    
    from app.api import register_api_routes
    register_api_routes(app)

    return app
