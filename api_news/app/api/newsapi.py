import time
import requests

from app.service.article_service import process_articles_batch

NEWS_API_KEY = '3ff7c545-1d93-4464-bbe3-fbc0c977954c'

def fetch_news_data():
    url = "https://eventregistry.org/api/v1/article/getArticles"
    articles_page = 1
    articles_count = 1
    while True:
        try:
            payload = {
                "action": "getArticles",
                "keyword": "terror attack",
                "ignoreSourceGroupUri": "paywall/paywalled_sources",
                "articlesPage": articles_page,
                "articlesCount": articles_count,
                "articlesSortBy": "socialScore",
                "articlesSortByAsc": False,
                "dataType": ["news", "pr"],
                "forceMaxDataTimeWindow": 31,
                "resultType": "articles",
                "apiKey": NEWS_API_KEY
            }
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                process_articles_batch(data['articles']['results'][0])
                articles_page += 1
            else:
                print(f"Request failed with status code {response.status_code}: {response.text}")
        except Exception as e:
            print("An error occurred:", str(e))
        time.sleep(120)