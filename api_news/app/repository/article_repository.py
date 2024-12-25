from typing import Dict, List

import toolz as t
from elasticsearch.helpers import bulk

from app.db.elastic_connect import elastic_client
from app.db.es_config import ARTICLE_INDEX


def insert_articles(articles_batch: List[Dict]):
    filtered_articles = t.pipe(
        articles_batch,
        t.partial(filter, lambda x: x is not None),
        list
    )

    actions = []

    for article in filtered_articles:

        action = {
            "_op_type": "index",
            "_index": ARTICLE_INDEX,
            "_id": article.get("url"),
            "_source": article
        }
        actions.append(action)

    try:
        success, failed = bulk(elastic_client, actions)
        return {"success": success, "failed": failed}
    except Exception as e:
        print(str(e))
        return {"success": 0, "failed": len(filtered_articles)}