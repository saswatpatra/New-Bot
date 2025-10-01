import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_bbc_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    response.raise_for_status()  # throw error if site not reachable

    soup = BeautifulSoup(response.text, "html.parser")

    # BBC headlines are usually in <h3> with class "gs-c-promo-heading__title"
    headlines = []
    for h3 in soup.find_all("h3", class_="gs-c-promo-heading__title"):
        text = h3.get_text(strip=True)
        if text and text not in headlines:  # avoid duplicates
            headlines.append(text)

    return headlines

def save_news(headlines):
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "headlines": headlines
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    news = scrape_bbc_news()
    save_news(news)
    print(f"✅ Scraped {len(news)} headlines and saved to news.json")
