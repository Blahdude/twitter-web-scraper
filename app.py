from flask import Flask, render_template, Response
import scrape  # Import your scraping module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape_and_analyze():
    results = scrape.main()
    return results

if __name__ == '__main__':
    app.run(debug=True)
