
from kafka import KafkaConsumer

TOPIC_NAME = 'test_topic'

def run_consumer() -> None:
	consumer = KafkaConsumer(TOPIC_NAME)

	for msg in consumer:
		print(msg)

if __name__ == '__main__':
	run_consumer()
