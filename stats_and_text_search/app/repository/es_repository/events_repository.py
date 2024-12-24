from app.settings.es_config import elastic_client as es

def search_keyword_in_events(word: str, limit: int, summary_boost: float = 2.0, custom_query_boost: float = 1.5):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": word,
                            "fields": [f"summary^{summary_boost}"]
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
        },
        "size": limit
    }
    response = es.search(index="events", body=query)
    hits = response['hits']['hits']
    return hits

def search_keyword_in_events_date_range(word: str, limit: int, start_year: int, start_month: int,
                                        end_year: int, end_month: int,
                                        summary_boost: float = 2.0):
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": word,
                            "fields": [f"summary^{summary_boost}"]
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "date.year": {
                                "gte": start_year,
                                "lte": end_year
                            }
                        }
                    },
                    {
                        "range": {
                            "date.month": {
                                "gte": start_month,
                                "lte": end_month
                            }
                        }
                    }
                ]
            }
        },
        "size": limit
    }
    response = es.search(index="events", body=query)
    hits = response['hits']['hits']
    return hits