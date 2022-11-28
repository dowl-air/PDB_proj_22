#!/bin/sh

cd "$(dirname "$0")"

if [ $# -gt 0 ] && [ "$1" = "-l" -o "$1" = "--local" ]; then
	export DB_HOST="localhost"

	export MONGODB_USERNAME=""
	export MONGODB_PASSWORD=""
	export MONGODB_HOSTNAME="localhost"

	export KAFKA_HOST="localhost"
	export KAFKA_PORT=9092
fi

pytest -W ignore::DeprecationWarning --verbose ./tests/ -rap
