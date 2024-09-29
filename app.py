from flask import Flask, request, jsonify
from scrapers.tiktok_video_downloader import get_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/api/download-tiktok-video', methods=['POST'])
def download_tiktok():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "No URL provided"}), 400
        
        url = data['url']
        result = get_data(url)

        if not result:
            return jsonify({"error": "Failed to retrieve data"}), 500
        elif 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
