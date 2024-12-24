from app.settings.es_config import elastic_client as es

def search_keyword_in_articles(word: str, title_boost: float = 2.0, body_boost: float = 1.0, custom_query_boost: float = 1.5):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": word,
                            "fields": [f"title^{title_boost}", f"body^{body_boost}"]
                        }
                    },
                    {
                        "match": {
                            "custom_field": {
                                "query": word,
                                "boost": custom_query_boost
                            }
                        }
                    }
                ]
            }
        }
    }
    response = es.search(index="articles", body=query)
    hits = response['hits']['hits']
    return hits

def build_date_range_filter(start_year: int, start_month: int, end_year: int, end_month: int) -> dict:
    start_date = None
    end_date = None

    if start_year is not None and start_month is not None:
        start_date = f"{start_year}-{start_month:02d}-01T00:00:00Z"

    if end_year is not None and end_month is not None:
        end_date = f"{end_year}-{end_month:02d}-01T23:59:59Z"

    date_range_filter = {}
    if start_date:
        date_range_filter["gte"] = start_date
    if end_date:
        date_range_filter["lte"] = end_date

    return date_range_filter

def search_keyword_in_articles_date_range(word: str, start_year: int, start_month: int, end_year: int, end_month: int, title_boost: float = 2.0, body_boost: float = 1.0, custom_query_boost: float = 1.5):
    date_range_filter = build_date_range_filter(start_year, start_month, end_year, end_month)
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": word,
                            "fields": [f"title^{title_boost}", f"body^{body_boost}"]
                        }
                    },
                    {
                        "match": {
                            "custom_field": {
                                "query": word,
                                "boost": custom_query_boost
                            }
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "dateTime": date_range_filter
                        }
                    }
                ]
            }
        }
    }
    response = es.search(index="articles", body=query)
    hits = response['hits']['hits']
    return hits