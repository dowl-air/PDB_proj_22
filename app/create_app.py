
from flask import Flask
import connexion

from appconfig import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
    MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOSTNAME, MONGODB_PORT, MONGODB_DATABASE
)

from entity.sql import db
from entity.sql.base import ma
from entity.nosql import mongo


def create_app() -> Flask:
    conn_app = connexion.App(__name__, specification_dir="./")
    conn_app.add_api("swagger.yml")

    app: Flask = conn_app.app

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MONGODB_SETTINGS'] = [
        {
            'username': MONGODB_USERNAME,
            'password': MONGODB_PASSWORD,
            'host': MONGODB_HOSTNAME,
            'port': MONGODB_PORT,
            'db': MONGODB_DATABASE
        }
    ]

    db.init_app(app)
    mongo.init_app(app)
    ma.init_app(app)

    @app.route("/")
    def hello_world(): # TODO
        return "Hello, World!"

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
