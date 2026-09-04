# routes.py
from flask import render_template, send_file

from app.data import Config, Videos


def register_routes(app):

    @app.route('/')
    def index():
        init_videos_count = Config.get_setting("init_videos_count")
        videos = _get_videos(0, init_videos_count)
        return render_template('index.html', videos=videos)


    @app.route('/watch/<string:video_id>')
    def watch(video_id):
        return render_template('watch.html', video_id=video_id)


    @app.route('/vids/<string:video_id>')
    def serve_video_file(video_id):
        video = Videos.get_video(video_id)

        if video:
            return send_file(video["path"])

        return "Invalid video file", 400


    @app.route('/settings')
    def settings():
        return render_template('settings.html')


def _get_videos(offset, limit):
    return Videos.get_videos(offset, limit)
