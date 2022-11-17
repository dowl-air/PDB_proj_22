FROM python:3.8.5-slim-buster

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000

CMD ["python", "./app/run.py"]