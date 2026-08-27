from flask import Flask, render_template, send_from_directory
import os
import json

app = Flask(__name__)

with open('settings.json') as f:
    config = json.load(f)

@app.route('/')
def index():
    videos = [
        {'id': 'XYb4zclX5-U','name': 'Video 1', 'full_name': 'ВОТ ПОЧЕМУ НЕ СТОИТ СТРОИТЬ ТЫСЯЧИ АЭРОПОРТОВ ｜ PLAGUE INC [XYb4zclX5-U].mkv', 'thumbnail': 'placeholder.png'},
        {'id': '','name': 'Video 2', 'full_name': 'vid.mkv', 'thumbnail': ''},
        {'id': 'wertt','name': 'Video 3', 'full_name': 'video3.mkv', 'thumbnail': ''},
    ]
    return render_template('index.html', videos=videos)

@app.route('/watch/<string:v>')
def watch(v):
    return render_template('watch.html', v=v)

@app.route('/vids/<string:v>')
def fetch_video(v):
    video_path = find_video(v)
    if video_path:
        return send_from_directory(os.path.dirname(video_path), os.path.basename(video_path))
    return "Invalid video file", 400

@app.route('/settings')
def settings():
    return render_template('settings.html')

def find_video(v):
    for directory in config.get('directories', []):
        for root, _, files in os.walk(directory):
            for filename in files:
                if v in filename:
                    return os.path.join(root, filename)
    return None

if __name__ == '__main__':
    app.run(debug=True)