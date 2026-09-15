# video.py
from flask import Blueprint, url_for, request
import logging

from app import video_metadata_service
from app import video_service
from app import config_service
from app.presentation.utils.responses import response_ok, response_err

log = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/videos/<video_id>/thumbnail')
def get_video_thumbnail(video_id):
    thumbnail, was_generated = video_metadata_service.fetch_thumbnail(video_id)

    if thumbnail is None: return response_err('Thumbnail generation failed', 404)

    thumbnail_url = url_for(
        'static',
        filename="thumbnails/" + thumbnail
    )

    return response_ok({ 'thumbnail_path': thumbnail_url, 'generated': was_generated })


@api_bp.route('/videos/<video_id>/duration')
def get_video_duration(video_id):
    duration, was_generated = video_metadata_service.fetch_duration(video_id)

    if duration is None: return response_err('Duration fetching failed', 404)

    return response_ok({ 'duration': duration, 'generated': was_generated })


@api_bp.route('/videos')
def fetch_videos():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    videos = video_service.get_banch_videos(offset, limit)

    return response_ok({ "videos": [video.to_dict() for video in videos] })


@api_bp.route('/config')
def get_config():
    config = config_service.get_all()

    return response_ok({ "config": config })
