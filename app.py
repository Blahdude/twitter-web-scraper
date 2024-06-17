from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import scrape

app = Flask(__name__, static_folder='react-scraper/build', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scrape', methods=['GET'])
def scrape_and_analyze():
    results = scrape.main()
    return jsonify({"data": results})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
