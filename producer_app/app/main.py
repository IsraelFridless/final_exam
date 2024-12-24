import logging
from dataclasses import asdict

from app.kafka_settings.producer import BatchKafkaProducer
from app.utils.data_convertion import extract_event_from_row

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    producer = BatchKafkaProducer(bootstrap_servers=['localhost:9092'])
    try:
        topics_mapping = {
            'regions': 'regions-topic',
            'countries': 'countries-topic'
        }
        producer.produce_json_to_topics(r'C:\Users\Python\final_exam\producer_app\app\datasets\regions.json', topics_mapping)
        producer.produce_json_to_topics(r'C:\Users\Python\final_exam\producer_app\app\datasets\countries.json', topics_mapping)

        csv_data = producer.load_data(r'C:\Users\Python\final_exam\producer_app\app\datasets\merged_file.csv', 'csv')
        events = [asdict(extract_event_from_row(row)) for row in csv_data]
        print(events[0])
        producer.produce_batch_data(
            data=events,
            topic='events-topic',
            batch_size=500,
            key_column='eventid'
        )

    except Exception as e:
        logger.error(f"Error in main processing: {str(e)}")
    finally:
        producer.close()


if __name__ == '__main__':
    main()