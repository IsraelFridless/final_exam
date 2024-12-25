import pandas as pd
import json
from typing import List, Dict

from elasticsearch.helpers import bulk

from app.db.elastic_connect import elastic_client
from app.db.es_config import EVENTS_INDEX


def clean_data(event: Dict) -> Dict:
    def clean_location(location: Dict) -> Dict:
        return {
            **location,
            'latitude': None if pd.isna(location.get('latitude')) else location.get('latitude'),
            'longitude': None if pd.isna(location.get('longitude')) else location.get('longitude')
        }

    def clean_field(field: str, value):
        return None if field in event and pd.isna(value) else value

    return {
        **event,
        'location': clean_location(event['location']) if 'location' in event else event.get('location'),
        'perpetrators': clean_field('perpetrators', event.get('perpetrators')),
        'summary': clean_field('summary', event.get('summary'))
    }


def insert_events_batch(events_batch: List[Dict]):
    def prepare_action(article: Dict) -> Dict:
        return {
            "_op_type": "index",
            "_index": EVENTS_INDEX,
            "_source": clean_data(article),
        }

    events_batch = json.loads(events_batch) if isinstance(events_batch, str) else events_batch

    actions = list(map(prepare_action, events_batch))

    try:
        success, failed = bulk(elastic_client, actions, raise_on_error=False)
        res = {"success": success, "failed": len(failed)}
        print(f'Inserted batch: {res}')

        if failed:
            print(f"Failed to index {len(failed)} documents.")
            for error in failed:
                print(f"Failed action: {error}")

        return res
    except Exception as e:
        print(f"Error during bulk insert: {str(e)}")
        return {"success": 0, "failed": len(events_batch)}