from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_page_structure(url):
    try:
        response = requests.get(url)
        if response.status_code!= 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        heading_paragraphs = {}
        for heading in headings:
            next_paragraph = heading.find_next('p')
            if next_paragraph:
                heading_paragraphs[heading.text.strip()] = next_paragraph.text.strip()
        return heading_paragraphs
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    return "Welcome to the web scraping API. Use the /scrape endpoint to scrape a webpage."

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Please provide a URL to scrape."})
    heading_paragraphs = extract_page_structure(url)
    if heading_paragraphs:
        return jsonify(heading_paragraphs)
    else:
        return jsonify({"error": "Failed to retrieve the webpage."})

if __name__ == '__main__':
    app.run(debug=True)