
from kafka import KafkaProducer

import os
from json import dumps

def create_producer() -> KafkaProducer:
    KAFKA_HOST = os.getenv('KAFKA_HOST', 'kafka')
    KAFKA_PORT = os.getenv('KAFKA_PORT', 29092)

    producer = KafkaProducer(
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        key_serializer=lambda x: bytes(x, encoding='utf8'),
        value_serializer=lambda x: dumps(x).encode('utf-8'),
        api_version=(0, 10, 2)
    )
    return producer
