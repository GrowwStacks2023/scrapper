from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    headings: dict

def extract_page_structure(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve the webpage. Status code: {response.status_code}")
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
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the web scraping API. Use the /scrape endpoint to scrape a webpage."}

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    heading_paragraphs = extract_page_structure(request.url)
    return heading_paragraphs
