
from flask import Flask
import os
import connexion

from entity.sql import db
from entity.sql.base import ma
from entity.nosql import mongo

MYSQL_DEFAULT_PORT = 3306
MONGO_DEFAULT_PORT = 27017


def create_app() -> Flask:
    conn_app = connexion.App(__name__, specification_dir="./")
    conn_app.add_api("swagger.yml")

    app: Flask = conn_app.app

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER', 'pdb'),
        os.getenv('DB_PASSWORD', 'pdb'),
        os.getenv('DB_HOST', 'mysql'),
        os.getenv('DB_PORT', MYSQL_DEFAULT_PORT),
        os.getenv('DB_NAME', 'pdb')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MONGODB_SETTINGS'] = [
        {
            'username': os.getenv('MONGODB_USERNAME', 'pdb'),
            'password': os.getenv('MONGODB_PASSWORD', 'pdb'),
            'host': os.getenv('MONGODB_HOSTNAME', 'mongodb'),
            'port': os.getenv('MONGODB_PORT', MONGO_DEFAULT_PORT),
            'db': os.getenv('MONGODB_DATABASE', 'pdb')
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
