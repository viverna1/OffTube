from flask import Flask, render_template, send_file, jsonify, url_for, request
import os

import file_manager

app = Flask(__name__)


@app.route('/')
def index():
    videos = file_manager.get_all_videos()
    return render_template('index.html', videos=videos)


@app.route('/watch/<string:v>')
def watch(v):
    return render_template('watch.html', v=v)


@app.route('/vids/<string:v>')
def fetch_video(v):
    video = file_manager.find_video(v)
    if video:
        return send_file(video["path"])
    return "Invalid video file", 400


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/generate-thumbnails-ajax', methods=['POST'])
def generate_thumbnails_ajax():
    # Получаем video_id из JSON-тела запроса
    data = request.get_json()
    video_id = data['video_id']
    
    # Находим видео
    video = file_manager.find_video(video_id)
    
    thumbnail_abs = file_manager.generate_thumbnail(video["path"])
    thumbnail_name = os.path.basename(thumbnail_abs)
    thumbnail_url = url_for('static', filename="thumbnails/" + thumbnail_name)     

    return jsonify({
        'status': 'success',
        'thumbnail_path': thumbnail_url
    })


if __name__ == '__main__':
    app.run(debug=True)