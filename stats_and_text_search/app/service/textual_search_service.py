from typing import Dict, List

from app.repository.es_repository.events_repository import *
from app.repository.es_repository.news_articles_repository import *


def format_search_results(results: List[Dict], result_type: str) -> List[Dict]:
    formatted_results = [
        {
            "type": result_type,
            "summary" if result_type == "event" else "title": result["_source"].get("summary") if result_type == "event" else result["_source"].get("title"),
            "body": result["_source"].get("body") if result_type == "article" else None,
            "latitude": result["_source"].get("location", {}).get("latitude"),
            "longitude": result["_source"].get("location", {}).get("longitude")
        }
        for result in results
        if (result["_source"].get("summary") or result["_source"].get("title") or result["_source"].get("body"))
        and result["_source"].get("location", {}).get("latitude") is not None
        and result["_source"].get("location", {}).get("longitude") is not None
    ]
    return formatted_results


def search_keyword_in_all_data_sources(keyword: str, limit: int) -> List[Dict]:
    events_result = search_keyword_in_events(keyword, limit)
    article_results = search_keyword_in_articles(keyword, limit)

    formatted_events = format_search_results(events_result, "event")
    formatted_articles = format_search_results(article_results, "article")

    return formatted_events + formatted_articles


def search_keyword_in_news_articles(keyword: str, limit: int) -> List[Dict]:
    article_results = search_keyword_in_articles(keyword, limit)
    return format_search_results(article_results, "article")


def search_keyword_in_historic_events(keyword: str, limit: int) -> List[Dict]:
    events_result = search_keyword_in_events(keyword, limit)
    return format_search_results(events_result, "event")


def search_results_by_date_range_all_sources(keyword: str, limit: int, start_year, start_month, end_year, end_month) -> List[Dict]:
    events_result = search_keyword_in_events_date_range(keyword, limit, start_year, start_month, end_year, end_month)
    article_results = search_keyword_in_articles_date_range(keyword, limit, start_year, start_month, end_year, end_month)

    formatted_events = format_search_results(events_result, "event")
    formatted_articles = format_search_results(article_results, "article")

    return formatted_events + formatted_articles