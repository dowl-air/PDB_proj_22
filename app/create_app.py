from flask import Flask
import os

from entity.sql import User


MYSQL_DEFAULT_PORT = 3306

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER', 'pdb'),
        os.getenv('DB_PASSWORD', 'pdb'),
        os.getenv('DB_HOST', 'mysql'),
        os.getenv('DB_PORT', MYSQL_DEFAULT_PORT),
        os.getenv('DB_NAME', 'pdb')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MONGO_URI'] = 'mongodb://{}:{}@{}:27017/{}'.format(
        os.getenv('MONGODB_USERNAME', 'pdb'),
        os.getenv('MONGODB_PASSWORD', 'pdb'),
        os.getenv('MONGODB_HOSTNAME', 'mongodb'),
        os.getenv('MONGODB_DATABASE', 'pdb')
    )

    from entity.sql import db
    db.init_app(app)

    from models_mongo import mongo
    mongo.init_app(app)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/users")
    def users():
        num_users = User.query.count()
        return f"Number of users: {num_users}"

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
