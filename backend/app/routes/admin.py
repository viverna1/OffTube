# admin.py
from flask import Blueprint
import logging

from app.data import Videos
from app.services import import_all_videos
from app.utils import response_err, response_ok


log = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/clear_cache', methods=['POST'])
def clear_cache():
    try:
        Videos.clear_cache()
        import_all_videos()

        log.info("Cache cleared and videos re-imported successfully.")
        return response_ok({ 'message': 'Cache cleared successfully.' })
    except Exception as e:
        log.exception("Error occurred while clearing cache")
        return response_err(str(e), 500)
