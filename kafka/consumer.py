
from kafka import KafkaConsumer

from kafka.consumer.fetcher import ConsumerRecord

TOPIC_NAME = 'test_topic'

KEY_DEFAULT = 'DEFAULT'
KEY_OTHER = 'OTHER'

def decode(x: bytes) -> str:
	return x.decode(encoding='utf8')

def run_consumer() -> None:
	consumer = KafkaConsumer(TOPIC_NAME)

	for msg in consumer:
		msg: ConsumerRecord

		topic = msg.topic
		key = decode(msg.key)
		value = decode(msg.value)
		print(f'{topic=}\t{key=}\t{value=}')

if __name__ == '__main__':
	run_consumer()
