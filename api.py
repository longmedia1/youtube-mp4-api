from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    ydl_opts = {
        'format': 'mp4',
        'quiet': True,
        'skip_download': True,
        'noplaylist': True,
        'forcejson': True,
        'extract_flat': False,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            for f in formats:
                if f.get('ext') == 'mp4' and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    return jsonify({
                        'title': info.get('title'),
                        'url': f.get('url')
                    })
            return jsonify({'error': 'No suitable MP4 format found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
