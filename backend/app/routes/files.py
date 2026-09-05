# files.py
from flask import Blueprint, send_file
import logging

from app.data import Videos

log = logging.getLogger(__name__)
files_bp = Blueprint('files', __name__, url_prefix='/files')


@files_bp.route('/video/<string:video_id>')
def serve_video_file(video_id):
    video = Videos.get_video(video_id)

    if video:
        return send_file(video["path"])

    return "Invalid video file", 404
