from app.db.elastic_connect import elastic_client

ARTICLE_INDEX = "articles"


def setup_article_index():
    if not elastic_client.indices.exists(index=ARTICLE_INDEX):
        elastic_client.indices.create(index=ARTICLE_INDEX, body={
            "mappings": {
                "properties": {
                    "dateTime": {
                        "type": "date",
                        "format": "strict_date_time"
                    },
                    "url": {
                        "type": "keyword"
                    },
                    "title": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "body": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "classification": {
                        "type": "keyword"
                    },
                    "location": {
                        "properties": {
                            "region": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
                            "country": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
                            "city": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                            },
                            "latitude": {
                                "type": "double"
                            },
                            "longitude": {
                                "type": "double"
                            }
                        }
                    }
                }
            }
        })