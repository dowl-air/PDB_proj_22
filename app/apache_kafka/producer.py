
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
def init_producer(producer: KafkaProducer, log: bool = True) -> KafkaProducer:
    _wait_for_bootstrap_connection(producer, log)
    _create_topics(log)

# little helper for optional non-error string print
def _log(msg: str, log: bool = True) -> None:
    if log:
        print(msg)

def _wait_for_bootstrap_connection(producer: KafkaProducer, log: bool = True) -> None:
    RETRY_DELAY = 3
    wait_time = 0
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
            _log(f'Producer: Waiting for Kafka bootstrap server connection {wait_time}s.', log)
            wait_time += RETRY_DELAY
            try:
                sleep(RETRY_DELAY)
            except KeyboardInterrupt:
                print('Producer: Initialization interrupted, exiting...')
                sys.exit(0)

    _log(f'Producer: Successfully connected to Kafka bootstrap server at {BOOTSTRAP_SERVER}.', log)

def _create_topics(log: bool = True) -> None:
    _log('Producer: Creating Kafka topics...', log)
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
    _log('Producer: Kafka topics were created or had already existed...', log)
