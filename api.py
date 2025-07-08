from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import re

app = Flask(__name__)

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta la URL'}), 400

    # 🔁 Convertir Shorts a formato estándar
    shorts_match = re.match(r'https?://(www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)', url)
    if shorts_match:
        video_id = shorts_match.group(2)
        url = f'https://www.youtube.com/watch?v={video_id}'

    output_filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': output_filename,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
