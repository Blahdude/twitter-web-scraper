from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import scrape

app = Flask(__name__, static_folder='react-scraper/build', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape_and_analyze():
    data = request.get_json()
    post_type = data.get('postType')
    
    if post_type == 'text':
        text = data.get('text')
        results = scrape.main('n/a', 'sentiment', text)  # Analyze the sentiment of the text
    else:
        url = data.get('url')
        results = scrape.main(url, post_type, 'n/a')
    
    return results  # Return the results as a plain string

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
