#!/bin/sh

cd "$(dirname "$0")"

export DB_HOST="localhost"
export MONGODB_USERNAME=""
export MONGODB_PASSWORD=""
export MONGODB_HOSTNAME="localhost"

pytest -W ignore::DeprecationWarning --verbose ./tests/ -rP
