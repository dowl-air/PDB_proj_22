FROM python:3.8.5-slim-buster

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "-u", "./app/run_consumer.py"]