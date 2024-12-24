from app.db.database import *
from app.db.repository.generic_repository import insert_batch_data


def process_batch(batch, topic):
    topic_to_collection = {
        'events-topic': events_collection,
        'regions-topic': regions_collection,
        'countries-topic': country_collection
    }

    collection_info = topic_to_collection.get(topic)

    if collection_info is None:
        raise ValueError(f"Unknown topic: {topic}.")

    return insert_batch_data(batch, collection_info)