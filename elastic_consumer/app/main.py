import sys
from kafka import KafkaConsumer
from app.db.es_config import setup_events_index, drop_index, EVENTS_INDEX
from app.repository.events_repository import insert_events_batch

topics = ['events-topic']
bootstrap_servers = ['localhost:9092', 'localhost:9093', 'localhost:9094']


def create_consumer():
    return KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        group_id='batch-kafka-elastic',
        auto_offset_reset='earliest',
    )


if __name__ == '__main__':
    setup_events_index()
    consumer = create_consumer()
    try:
        print(f"Subscribed to topics: {topics}")

        for message in consumer:
            try:
                message_value = message.value.decode('utf-8')
                insert_events_batch(message_value)

            except Exception as e:
                print(f"Error processing message: {e}")
                continue

    except KeyboardInterrupt:
        print('\nStopping consumer...')
        sys.exit(0)
    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
    finally:
        if consumer:
            consumer.close()
            print("Kafka consumer closed.")
