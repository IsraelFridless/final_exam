from app.db.elastic_connect import elastic_client

EVENTS_INDEX = 'events'

def setup_events_index():
    if not elastic_client.indices.exists(index=EVENTS_INDEX):
        mapping = {
            "mappings": {
                "properties": {
                    "date": {
                        "type": "object",
                        "properties": {
                            "year": { "type": "integer" },
                            "month": { "type": "integer" },
                            "day": { "type": "integer" }
                        }
                    },
                    "location": {
                        "type": "object",
                        "properties": {
                            "region": {"type": "keyword"},
                            "country": {"type": "keyword"},
                            "city": {"type": "keyword"},
                            "latitude": {"type": "float"},
                            "longitude": {"type": "float"}
                        }
                    },
                    "perpetrators": {
                        "type": "integer"
                    },
                    "groups_involved": {
                        "type": "keyword"
                    },
                    "attack_types": {
                        "type": "keyword"
                    },
                    "target_types": {
                        "type": "keyword"
                    },
                    "casualties": {
                        "type": "object",
                        "properties": {
                            "fatalities": {"type": "integer"},
                            "injuries": {"type": "integer"}
                        }
                    },
                    "summary": {
                        "type": "text"
                    }
                }
            }
        }

        elastic_client.indices.create(index=EVENTS_INDEX, body=mapping)
        print(f"Index '{EVENTS_INDEX}' created successfully.")
    else:
        print(f"Index '{EVENTS_INDEX}' already exists.")

def drop_index(index_name: str):
    try:
        if elastic_client.indices.exists(index=index_name):
            elastic_client.indices.delete(index=index_name)
            print(f"Index '{index_name}' has been deleted successfully.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"Error while deleting index '{index_name}': {str(e)}")