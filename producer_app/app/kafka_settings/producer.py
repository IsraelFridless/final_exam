from kafka import KafkaProducer
import json
import pandas as pd
import logging
from typing import List, Any, Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchKafkaProducer:
    def __init__(self, bootstrap_servers: List[str]):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            key_serializer=lambda x: x.encode('utf-8') if x else None,
            batch_size=16384,
            linger_ms=100,
            compression_type='gzip'
        )

    @staticmethod
    def load_data(file_path: str, file_type: str = 'csv') -> Any:
        try:
            if file_type == 'csv':
                return pd.read_csv(file_path, encoding='iso-8859-1').to_dict('records')
            elif file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise

    def produce_batch_data(self,
                           data: List[Dict],
                           topic: str,
                           batch_size: int = 500,
                           key_column: Optional[str] = None) -> None:
        batch = []
        last_row_key = None
        total_records = 0

        try:
            for item in data:
                batch.append(item)
                if key_column and isinstance(item, dict) and key_column in item:
                    last_row_key = str(item[key_column])

                if len(batch) >= batch_size:
                    self._send_batch(topic, batch, last_row_key)
                    total_records += len(batch)
                    logger.info(f"Sent batch of {len(batch)} records to topic {topic}. "
                                f"Total records sent: {total_records}")
                    batch = []

            if batch:
                self._send_batch(topic, batch, last_row_key)
                total_records += len(batch)
                logger.info(f"Sent final batch of {len(batch)} records to topic {topic}. "
                            f"Total records sent: {total_records}")

        except Exception as e:
            logger.error(f"Error producing batch to topic {topic}: {str(e)}")
            raise
        finally:
            self.producer.flush()

    def _send_batch(self, topic: str, batch: List[Dict], key: Optional[str]) -> None:
        try:
            future = self.producer.send(topic, key=key, value=batch)
            future.get(timeout=60)
        except Exception as e:
            logger.error(f"Failed to send batch to topic {topic}: {str(e)}")
            raise

    def produce_json_to_topics(self, file_path: str, topics_mapping: Dict[str, str]) -> None:
        try:
            data = self.load_data(file_path, file_type='json')
            for key, topic in topics_mapping.items():
                if key in data:
                    logger.info(f"Processing data for topic {topic} from key {key}")
                    self.produce_batch_data(data[key], topic)
                else:
                    logger.warning(f"Key {key} not found in JSON data")

        except Exception as e:
            logger.error(f"Error processing JSON file {file_path}: {str(e)}")
            raise

    def close(self):
        self.producer.close()