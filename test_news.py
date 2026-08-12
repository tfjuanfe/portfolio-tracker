import requests
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\Sarpantu\Desktop\Portfolio Tracker Project\.env")
api_key = os.getenv("NEWS_API_KEY")
url = f"https://newsapi.org/v2/everything?q=finance&apiKey={api_key}&pageSize=1"
rsp = requests.get(url).json()

article = rsp["articles"][0]
print("DESC:", article.get("description"))
print("CONTENT:", article.get("content"))
