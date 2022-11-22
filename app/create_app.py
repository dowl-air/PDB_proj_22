
from flask import Flask
import os
import connexion

from entity.sql import db, ma
from entity.nosql import mongo

from entity.sql import User, Book
from entity.nosql import Book as MongoBook


MYSQL_DEFAULT_PORT = 3306
MONGO_DEFAULT_PORT = 27017


def create_app():
    conn_app = connexion.App(__name__, specification_dir="./")
    conn_app.add_api("swagger.yml")

    app = conn_app.app

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
    def hello_world():
        return "Hello, World!"

    @app.route("/users")
    def users():
        num_users = User.query.count()
        return f"Number of users: {num_users}"

    @app.route('/add_book/<id>')
    def add_book(id):
        book = MongoBook(id=id, name=id)
        try:
            book.save(force_insert=True)
        except:
            return f'Duplicate book id: {id}'

        return f'Added new book: {id}'

    @app.route('/create_book')
    def create_book(object):
        pass

    @app.route('/books')
    def books():
        """ books = MongoBook.objects()
        book_names = [book.name for book in books]
        return f'Book names: {book_names}' """
        books = Book.query.all()
        return books_schema.dump(books)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
