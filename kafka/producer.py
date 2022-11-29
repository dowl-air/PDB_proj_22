
from kafka import KafkaProducer
from json import dumps
TOPIC_NAME = 'test_topic'

KEY_DEFAULT = 'DEFAULT'
KEY_OTHER = 'OTHER'


def encode(x: str) -> bytes:
    return bytes(x, encoding='utf8')


def run_producer() -> None:
    producer = KafkaProducer(
        bootstrap_servers=['kafka:29092'],
        key_serializer=lambda x: bytes(x, encoding='utf8'),
        value_serializer=lambda x: dumps(x).encode('utf-8'),
        api_version=(0, 10, 2)
    )
    while True:
        x = input('>')

        if len(x) < 1:
            continue
        if x == 'exit':
            return

        obj = {
            "message": x
        }

        key = KEY_OTHER if x[0].lower() == 'o' else KEY_DEFAULT

        producer.send("author", obj, key=KEY_DEFAULT)


if __name__ == '__main__':
    run_producer()
