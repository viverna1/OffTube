from flask import jsonify, url_for, request

from app.data import Config, Videos
import app.services.video_metadata as video_metadata
import app.utils as utils


def register_api_routes(app):
    @app.route('/api/videos/<video_id>/thumbnail')
    def api_get_video_thumbnail(video_id):
        thumbnail, was_generated = video_metadata.fetch_thumbnail(video_id)

        if thumbnail is None:
            return jsonify({
                'ok': False,
                'error': 'Thumbnail generation failed'
            }), 404

        thumbnail_url = url_for(
            'static',
            filename="thumbnails/" + thumbnail
        )

        return jsonify({
            'ok': True,
            'data': {
                'thumbnail_path': thumbnail_url,
                'generated': was_generated
            }
        })


    @app.route('/api/videos/<video_id>/duration')
    def api_get_video_duration(video_id):
        duration, was_generated = video_metadata.fetch_duration(video_id)

        if duration is None:
            return jsonify({
                'ok': False,
                'error': 'Duration fetching failed'
            }), 404

        return jsonify({
            'ok': True,
            'data': {
                'duration': duration,
                'generated': was_generated
            }
        })


    @app.route('/api/videos')
    def api_get_videos():
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)

        videos = _get_videos(offset, limit)

        return jsonify({
            "ok": True,
            "data": {
                "videos": videos
            }
        })


    @app.route('/api/config')
    def get_config():
        config = Config.get_all()

        return jsonify({
            "ok": True,
            "data": {
                "config": config
            }
        })


def _get_videos(offset, limit):
    return Videos.get_videos(offset, limit)
