from flask import Flask, render_template, send_file, send_from_directory, jsonify, url_for, request
import os

from core.data import Videos
import core.file_manager as file_manager
import core.thumbnail_generator as thumbnail_generator
import core.utils as utils


app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/')
def index():
    videos = Videos.get_all()
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


# ==================== POSTs ====================
@app.route('/fetch-thumbnail-ajax', methods=['POST'])
def fetch_thumbnail_ajax():
    data = request.get_json()
    video_id = data['video_id']

    thumbnail_abs, was_generated = thumbnail_generator.fetch_thumbnail(video_id)
    
    if not thumbnail_abs:
        return jsonify({'status': 'error', 'message': 'Thumbnail generation failed'}), 404

    thumbnail_url = url_for('static', filename="thumbnails/" + os.path.basename(thumbnail_abs))

    return jsonify({
        'status': 'success',
        'thumbnail_path': thumbnail_url,
        'generated': was_generated  # True - создано сейчас, False - уже существовало
    })


@app.route('/fetch-duration-ajax', methods=['POST'])
def fetch_duration_ajax():
    data = request.get_json()
    video_id = data['video_id']

    duration, was_generated = file_manager.fetch_duration(video_id)
    
    if not duration:
        return jsonify({'status': 'error', 'message': 'Duration fetching failed'}), 404
    
    return jsonify({
        'status': 'success',
        'duration': utils.formate_time(duration),
        'generated': was_generated  # True - создано сейчас, False - уже существовало
    })


if __name__ == '__main__':
    file_manager.generate_all_videos()
    app.run(debug=True)
