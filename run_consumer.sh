#!/bin/sh

cd "$(dirname "$0")"

export MONGODB_USERNAME=""
export MONGODB_PASSWORD=""
export MONGODB_HOSTNAME="localhost"

export KAFKA_HOST="localhost"
export KAFKA_PORT=9092

python3 ./app/run_consumer.py
