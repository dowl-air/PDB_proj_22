#!/bin/sh

cd "$(dirname "$0")"

if [ $# -gt 0 ] && [ "$1" = "-l" -o "$1" = "--local" ]; then
	export DB_HOST="localhost"
	export MONGODB_USERNAME=""
	export MONGODB_PASSWORD=""
	export MONGODB_HOSTNAME="localhost"
fi

PYTHONPATH=./:./app python3 ./tests/data.py
