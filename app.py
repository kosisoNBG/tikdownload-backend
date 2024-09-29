from flask import Flask, request, jsonify
from scrapers.tiktok_video_downloader import get_data
from flask_cors import CORS



app = Flask(__name__)

# Enable CORS for all routes and allow localhost:3000 (React default port)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# TikTok Scraper Route
@app.route('/api/download-tiktok', methods=['POST'])
def download_tiktok():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    result = get_data(url)
    
    if 'error' in result:
        return jsonify({"error": result['error']}), 400
    
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
