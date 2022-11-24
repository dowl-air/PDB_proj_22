
from kafka import KafkaProducer

TOPIC_NAME = 'test_topic'

KEY_DEFAULT = 'DEFAULT'
KEY_OTHER = 'OTHER'

def encode(x: str) -> bytes:
	return bytes(x, encoding='utf8')

def run_producer() -> None:
	producer = KafkaProducer()
	while True:
		x = input('>')

		if len(x) < 1:
			continue
		if x == 'exit':
			return

		key = KEY_OTHER if x[0].lower() == 'o' else KEY_DEFAULT

		producer.send(TOPIC_NAME, encode(x), key=encode(key))

if __name__ == '__main__':
	run_producer()
