
from kafka import KafkaProducer

TOPIC_NAME = 'test_topic'

def run_producer() -> None:
	producer = KafkaProducer()
	while True:
		x = input('>')
		if(x == 'exit'):
			return
		producer.send(TOPIC_NAME, bytes(x, encoding='utf8'))

if __name__ == '__main__':
	run_producer()
