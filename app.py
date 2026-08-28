from flask import Flask, render_template, send_file, jsonify, url_for, request
import os

from core.data import Videos, Config
import core.file_manager as file_manager
import core.video_metadata as video_metadata
import core.utils as utils


app = Flask(__name__)


@app.route('/')
def index():
    Videos.reset_counter()
    init_videos_count = Config.get_setting("init_videos_count")
    videos = Videos.get_videos(init_videos_count) or []
    return render_template('index.html', videos=videos)


@app.route('/watch/<string:video_id>')
def watch(video_id):
    return render_template('watch.html', video_id=video_id)


@app.route('/vids/<string:video_id>')
def fetch_video(video_id):
    video = Videos.get_video(video_id)
    if video:
        return send_file(video["path"])
    return "Invalid video file", 400


@app.route('/settings')
def settings():
    return render_template('settings.html')


# ==================== API ====================
@app.route('/api/videos/<video_id>/thumbnail')
def fetch_thumbnail_ajax(video_id):
    thumbnail, was_generated = video_metadata.fetch_thumbnail(video_id)
    
    if thumbnail is None:
        return jsonify({'ok': False, 'error': 'Thumbnail generation failed'}), 404

    thumbnail_url = url_for('static', filename="thumbnails/" + thumbnail)

    return jsonify({
        'ok': True,
        "data": {
            'thumbnail_path': thumbnail_url,
            'generated': was_generated  # True - создано сейчас, False - уже существовало
        }
    })


@app.route('/api/videos/<video_id>/duration')
def fetch_duration_ajax(video_id):
    duration, was_generated = video_metadata.fetch_duration(video_id)
    
    if duration is None:
        return jsonify({'ok': False, 'error': 'Duration fetching failed'}), 404
    
    return jsonify({
        'ok': True,
        "data": {
            'duration': duration,
            'generated': was_generated  # True - создано сейчас, False - уже существовало
        }
    })


@app.route('/api/videos')
def get_videos():
    videos_per_scroll = Config.get_setting("videos_per_scroll")
    videos = Videos.get_videos(videos_per_scroll)

    return jsonify({
        "ok": True,
        "data": {
            "videos": videos
        }
    })


if __name__ == '__main__':
    file_manager.generate_all_videos()
    app.run(debug=True)
