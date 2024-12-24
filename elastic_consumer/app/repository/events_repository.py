import pandas as pd
import json
from typing import List, Dict

from elasticsearch.helpers import bulk

from app.db.elastic_connect import elastic_client
from app.db.es_config import EVENTS_INDEX


def clean_data(event: Dict) -> Dict:
    if 'location' in event:
        location = event['location']
        if 'latitude' in location and pd.isna(location['latitude']):
            location['latitude'] = None
        if 'longitude' in location and pd.isna(location['longitude']):
            location['longitude'] = None

    if 'perpetrators' in event and pd.isna(event['perpetrators']):
        event['perpetrators'] = None

    if 'summary' in event and pd.isna(event['summary']):
        event['summary'] = None

    return event


def insert_events_batch(events_batch: List[Dict]):
    if isinstance(events_batch, str):
        events_batch = json.loads(events_batch)

    actions = []
    for article in events_batch:
        article = clean_data(article)

        action = {
            "_op_type": "index",
            "_index": EVENTS_INDEX,
            "_source": article
        }
        actions.append(action)

    try:
        success, failed = bulk(elastic_client, actions, raise_on_error=False)
        res = {"success": success, "failed": len(failed)}
        print(f'inserted batch: {res}')
        if len(failed) > 0:
            print(f"Failed to index {len(failed)} documents.")
            for error in failed:
                print(f"Failed action: {error}")

        return res
    except Exception as e:
        print(f"Error during bulk insert: {str(e)}")
        return {"success": 0, "failed": len(events_batch)}