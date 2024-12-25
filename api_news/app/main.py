import sys

from app.api.newsapi import fetch_news_data
from app.db.es_config import setup_article_index

if __name__ == '__main__':
    try:
        setup_article_index()
        fetch_news_data()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)