
from kafka import KafkaConsumer
from json import loads
from kafka.consumer.fetcher import ConsumerRecord

TOPIC_NAME = 'test_topic'

KEY_DEFAULT = 'DEFAULT'
KEY_OTHER = 'OTHER'


def decode(x: bytes) -> str:
    return x.decode(encoding='utf8')


def run_consumer() -> None:
    consumer = KafkaConsumer(
        "pdb",
        bootstrap_servers=['kafka:29092'],
        key_deserializer=lambda x: x.decode(),
        value_deserializer=lambda x: loads(x.decode("utf-8")),
        api_version=(0, 10, 2)
    )

    for msg in consumer:
        msg: ConsumerRecord
        print(msg)
        topic = msg.topic
        key = msg.key
        value = msg.value
        print(f'{topic=}\t{key=}\t{value=}')


if __name__ == '__main__':
    run_consumer()
