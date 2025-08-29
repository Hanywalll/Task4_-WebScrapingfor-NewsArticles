from flask import Flask, render_template, request, jsonify
from scraper import DetikScraper

app = Flask(__name__)
scraper = DetikScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_articles():
    query = request.form.get('query')
    if not query or not query.strip():
        return jsonify({"error": "Query is required"}), 400

    try:
        articles = scraper.scrape_search_results(query.strip())
        return jsonify(articles)
    except Exception as e:
        print(f"Error in search: {e}")
        return jsonify({"error": "Terjadi kesalahan internal server"}), 500

if __name__ == '__main__':
    app.run(debug=True)