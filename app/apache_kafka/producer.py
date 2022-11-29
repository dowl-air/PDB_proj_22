
from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError
from kafka.admin import NewTopic

import sys
from json import dumps
from time import sleep

from appconfig import KAFKA_HOST, KAFKA_PORT

from apache_kafka.enums import KafkaTopic

BOOTSTRAP_SERVER = f'{KAFKA_HOST}:{KAFKA_PORT}'
API_VERSION = (0, 10, 2)

def create_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=[BOOTSTRAP_SERVER],
        key_serializer=lambda x: bytes(x, encoding='utf8'),
        value_serializer=lambda x: dumps(x).encode('utf-8'),
        api_version=API_VERSION
    )

    return producer

# waits for the bootstrap broker to start and creates all topics
def init_producer(producer: KafkaProducer) -> KafkaProducer:
    _wait_for_bootstrap_connection(producer)
    _create_topics()

def _wait_for_bootstrap_connection(producer: KafkaProducer) -> None:
    RETRY_DELAY = 3
    waittime = 0
    while True:
        try:
            version = producer._sender._client.check_version()
        # not a problem, wait for the broker to start
        except NoBrokersAvailable:
            version = None
        except Exception as exc:
            print('Producer: Initialization error: ', exc)

        if version is not None:
            break
        else:
            print(f'Producer: Waiting for Kafka bootstrap server connection {waittime}s.')
            waittime += RETRY_DELAY
            try:
                sleep(RETRY_DELAY)
            except KeyboardInterrupt:
                print('Producer: Producer initialization interrupted, exiting...')
                sys.exit(0)

    print(f'Producer: Successfully connected to Kafka bootstrap server at {BOOTSTRAP_SERVER}.')

def _create_topics() -> None:
    print('Producer: Creating Kafka topics...')
    admin = KafkaAdminClient(
        bootstrap_servers=[BOOTSTRAP_SERVER],
        api_version=API_VERSION
    )

    # assumes that the connection is established
    try:
        # create all required Kafka topics
        admin.create_topics([NewTopic(topic.value, 1, 1) for topic in KafkaTopic])
    # not a problem, since we only want to ensure that the topics exist
    except TopicAlreadyExistsError:
        pass
    print('Producer: Kafka topics were created or had already existed...')
