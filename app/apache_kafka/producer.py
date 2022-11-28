
from kafka import KafkaProducer

from json import dumps

from appconfig import KAFKA_HOST, KAFKA_PORT

def create_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        key_serializer=lambda x: bytes(x, encoding='utf8'),
        value_serializer=lambda x: dumps(x).encode('utf-8'),
        api_version=(0, 10, 2)
    )
    return producer
