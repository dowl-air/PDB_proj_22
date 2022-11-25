from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from json import loads

from enums import KafkaKey, KafkaTopic

""" TOPIC_NAME = 'test_topic'

KEY_DEFAULT = 'DEFAULT'
KEY_OTHER = 'OTHER' """


""" def decode(x: bytes) -> str:
    return x.decode(encoding='utf8') """


def manage_author(value, key):
    if (key == KafkaKey.CREATE):
        pass


func_dict = {
    KafkaTopic.AUTHOR: manage_author
}


def run_consumer() -> None:
    consumer = KafkaConsumer(
        "global",
        bootstrap_servers=['kafka:9092'],
        key_deserializer=lambda x: x.decode(),
        value_deserializer=lambda x: loads(x.decode("utf-8"))
    )
    consumer.subscribe([t.value for t in KafkaTopic])

    for msg in consumer:
        msg: ConsumerRecord
        print(msg)
        func_dict[topic](value=msg.v, key=msg.key)

        topic = msg.topic
        key = msg.key
        value = msg.value
        print(f'{topic=}\t{key=}\t{value=}')


if __name__ == '__main__':
    run_consumer()
