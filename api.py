from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'mp4',
        'extract_flat': 'in_playlist',
        'skip_download': True,
        'forcejson': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])
            video_url = next((f['url'] for f in formats if f.get('ext') == 'mp4' and f.get('vcodec') != 'none'), None)

            if video_url:
                return jsonify({'download_url': video_url})
            else:
                return jsonify({'error': 'No MP4 URL found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
