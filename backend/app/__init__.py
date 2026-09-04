from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    from app.routes import register_routes
    register_routes(app)
    
    from app.api import register_api_routes
    register_api_routes(app)

    return app
