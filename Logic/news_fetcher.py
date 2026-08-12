import requests
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_financial_news():
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
        api_key = os.getenv("NEWS_API_KEY")

        if not api_key:
            print("NEWS_API_KEY not found in .env file")
            return []

        url = (
            "https://newsapi.org/v2/everything?"
            "q=stocks+finance+investing+crypto&"
            "language=en&"
            "sortBy=publishedAt&"
            "pageSize=20&"
            f"apiKey={api_key}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if data["status"] != "ok":
            return []

        articles = []
        for article in data["articles"]:
            if article["title"] and article["title"] != "[Removed]":
                articles.append({
                    "title":       article["title"],
                    "source":      article["source"]["name"],
                    "description": article.get("description", "No description available."),
                    "content":     article.get("content", "No content available."),
                    "url":         article.get("url", ""),
                    "publishedAt": article.get("publishedAt", "")[:10]
                })
        return articles

    except Exception as e:
        print(f"News fetch error: {e}")
        return []
