SHELL := /bin/bash

# build and run dockerized app
all: build run

# install venv and dependencies
venv: venv/create venv/touchfile

venv/create: 
	test -d venv || python3 -m venv venv

# only install dependencies when requirements.txt changes
venv/touchfile: server/requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur server/requirements.txt
	touch venv/touchfile

test: venv
	. venv/bin/activate; nosetests /test

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

# Build the docker application
build:
	docker-compose build

#Run the Docker application
run:
	docker-compose up
