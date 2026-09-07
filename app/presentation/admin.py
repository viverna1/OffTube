# admin.py
from flask import Blueprint
import logging

from app.application.video_service import videoService
from app.application import video_importer
from app.utils import response_err, response_ok, reset_id


log = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/clear_cache')
def clear_videos_cache():
    try:
        reset_id()
        videoService.clear_cache()
        video_importer.sync_videos()

        log.info("Cache cleared and videos re-imported successfully.")
        return response_ok({ 'message': 'Cache cleared successfully.' })
    except Exception as e:
        log.exception("Error occurred while clearing cache")
        return response_err(str(e), 500)
