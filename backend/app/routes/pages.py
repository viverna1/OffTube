# routes.py
from flask import Blueprint, render_template
import logging

from app.data import Config, Videos

log = logging.getLogger(__name__)
pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    init_videos_count = Config.get_setting("init_videos_count")
    videos = Videos.get_videos(0, init_videos_count)
    return render_template('index.html', videos=videos)


@pages_bp.route('/watch/<string:video_id>')
def watch(video_id):
    video = Videos.get_video(video_id)

    if not video:
        return "Video not found", 404

    return render_template('watch.html', video=video)


@pages_bp.route('/settings')
def settings():
    return render_template('settings.html')
