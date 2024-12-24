import sys

from app.service.process_data import process_batch
from kafka import KafkaConsumer

topics = [
    'events-topic',
    'regions-topic',
    'countries-topic'
]

bootstrap_servers = ['localhost:9092', 'localhost:9093', 'localhost:9094']

consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=bootstrap_servers,
    group_id='batch-kafka-mongo',
    auto_offset_reset='earliest'
)

if __name__ == '__main__':
    try:
        print(f"Subscribed to topics: {topics}")
        for message in consumer:
            process_batch(message.value.decode('utf-8'), topic=message.topic)
    except KeyboardInterrupt:
        print('\nStopping consumer...')
        sys.exit(0)
    finally:
        consumer.close()