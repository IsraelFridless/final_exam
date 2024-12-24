import json
from typing import List


def insert_batch_data(batch: List[dict], collection):
    if isinstance(batch, str):
        batch = json.loads(batch)
    try:
        collection.insert_many(batch)
        print(f"{len(batch)} records inserted into {collection.name} collection successfully.")

    except Exception as e:
        print(f"Error inserting teacher data: {e}")