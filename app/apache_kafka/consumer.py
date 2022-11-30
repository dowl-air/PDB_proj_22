
from kafka import KafkaConsumer
import mongoengine as me

import signal
import sys
from json import loads
from time import sleep

from appconfig import (
    MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOSTNAME, MONGODB_PORT, MONGODB_DATABASE,
    KAFKA_HOST, KAFKA_PORT
)

from apache_kafka.enums import KafkaKey, KafkaTopic

from entity import ReservationState, BorrowalState

from entity.nosql.author import Author
from entity.nosql.book import Book
from entity.nosql.book_copy import BookCopy
from entity.nosql.category import Category
from entity.nosql.location import Location
from entity.nosql.review import Review
from entity.nosql.user import User
from entity.nosql.reservation import Reservation
from entity.nosql.borrowal import Borrowal
from entity.nosql.schemas_mongo import author_schema, books_schema, category_schema, book_copy_schema, location_schema, book_copy_schema, book_schema, review_schema, user_schema, reservation_schema, borrowal_schema, user_schema


def manage_author(key, value):
    if (key == KafkaKey.CREATE.value):
        # create new author object
        author = author_schema.load(value)
        author.save()

    if (key == KafkaKey.UPDATE.value):
        # update author object itself
        author = Author.objects(id=int(value["id"])).first()
        author.update(**value)

        # we dont want to add books and description
        if "books" in value:
            del value["books"]
        if "description" in value:
            del value["description"]

        # update each book that holds this author
        books = Book.objects(authors__id=int(value["id"]))
        for book in books:
            # for each book update author by author id
            author_object = next((a for a in book.authors if a.id == int(value["id"])), None)
            if author_object:
                book.authors.remove(author_object)
                book.authors.append(value)
            book.update(authors=book.authors)

    if (key == KafkaKey.DELETE.value):
        # delete author object itself
        author = Author.objects(id=int(value["id"])).first().delete()

        # delete author object from books
        books = Book.objects(authors__id=int(value["id"]))
        for book in books:
            # for each book delete author by author id
            author_object = next((x for x in book.authors if x.id == int(value["id"])), None)
            if author_object:
                book.authors.remove(author_object)
            book.update(authors=book.authors)


def manage_category(key, value):
    if (key == KafkaKey.CREATE.value):
        # create new category object
        c = category_schema.load(value)
        c.save()

    if (key == KafkaKey.UPDATE.value):
        # update category object itself
        c = Category.objects(id=int(value["id"])).first()
        c.update(**value)

        """         # we dont want to add books and description
        if "books" in value:
            del value["books"]"""
        if "description" in value:
            del value["description"]

        # update each book that holds this category
        books = Book.objects(categories__id=int(value["id"]))
        for book in books:
            # for each book update category by category id
            cat = next((a for a in book.categories if a.id == int(value["id"])), None)
            if cat:
                book.categories.remove(cat)
                book.categories.append(value)
            book.update(categories=book.categories)

    if (key == KafkaKey.DELETE.value):
        # delete category object itself
        c = Category.objects(id=int(value["id"])).first().delete()

        # delete categ object from books
        books = Book.objects(categories__id=int(value["id"]))
        for book in books:
            # for each book delete cat by cat id
            cat = next((x for x in book.categories if x.id == int(value["id"])), None)
            if cat:
                book.categories.remove(cat)
            book.update(categories=book.categories)


def manage_location(key, value):
    if (KafkaKey.CREATE.value == key):
        l = location_schema.load(value)
        l.save()

    if (KafkaKey.UPDATE.value == key):
        # update location object itself
        l = Location.objects(id=int(value["id"])).first()
        l.update(**value)

        # update each book_copy object
        books = BookCopy.objects(location__id=int(value["id"]))
        for book in books:
            # for each book update location
            book.update(location=value)

    if (KafkaKey.DELETE.value == key):
        # delete location object itself
        l = Location.objects(id=int(value["id"])).first().delete()


def manage_book_copy(key, value):
    if (KafkaKey.CREATE.value == key):
        # insert to book
        book = Book.objects(id=int(value["book_id"])).first()
        book.book_copies.append(value)
        book.update(book_copies=book.book_copies)

        if "location_id" in value:
            location_id = int(value["location_id"])
            del value["location_id"]
            location = Location.objects(id=location_id).first()
            value["location"] = location_schema.dump(location)

        l = book_copy_schema.load(value)
        l.save()

    if (KafkaKey.UPDATE.value == key):
        books = Book.objects(book_copies__id=int(value["id"]))
        for book in books:
            cat = next((a for a in book.book_copies if a.id == int(value["id"])), None)
            if cat:
                book.book_copies.remove(cat)
                if int(value["book_id"]) == int(book.id):
                    # insert this book copy only if book_id is equal to book.id, otherwise just delete
                    book.book_copies.append(value)
            book.update(book_copies=book.book_copies)

            # if book_id changed, update new book
            new_book = Book.objects(id=int(value["book_id"])).first()
            if new_book:
                existing_book_copy = next((a for a in new_book.book_copies if a.id == int(value["id"])), None)
                if not existing_book_copy:
                    new_book.book_copies.append(value)
                    new_book.update(book_copies=new_book.book_copies)

        if "location_id" in value:
            location_id = int(value["location_id"])
            del value["location_id"]
            location = Location.objects(id=location_id).first()
            value["location"] = location_schema.dump(location)

        l = BookCopy.objects(id=int(value["id"])).first()
        l.update(**value)

    if (KafkaKey.DELETE.value == key):
        l = BookCopy.objects(id=int(value["id"])).first().delete()


def manage_book(key, value):
    # delete reviews
    if "reviews" in value:
        del value["reviews"]

    # rename copies -> book_copies
    if "copies" in value:
        value["book_copies"] = value["copies"]
        del value["copies"]

    if (KafkaKey.UPDATE.value == key or KafkaKey.DELETE.value == key):
        # remove this book object from all authors first
        authors = Author.objects(books__id=int(value["id"]))
        for author in authors:
            book = next((a for a in author.books if a.id == int(value["id"])), None)
            if book:
                author.books.remove(book)
                author.update(books=author.books)

    if (KafkaKey.DELETE.value == key):
        # delete book itself
        return Book.objects(id=int(value["id"])).first().delete()

    value_for_author = {
        "ISBN": value["ISBN"],
        "release_date": value["release_date"],
        "id": value["id"],
        "name": value["name"],
        "description": value["description"] if "description" in value else ""
    }

    # reformat authors field
    if "authors" in value:
        for idx, author_id in enumerate(value["authors"]):
            author = Author.objects(id=int(author_id)).first()
            if author:
                # update book object
                value["authors"][idx] = author_schema.dump(author)
                if "books" in value["authors"][idx]:
                    del value["authors"][idx]["books"]

                # update author object (propagate)
                author_books_list = author.books if author.books else []
                author_books_list.append(value_for_author)
                author.update(books=author_books_list)

    # reformat categories field
        if "categories" in value:
            for idx, category_id in enumerate(value["categories"]):
                cat = Category.objects(id=int(category_id)).first()
                if cat:
                    value["categories"][idx] = category_schema.dump(cat)

    if (KafkaKey.CREATE.value == key):
        l = book_schema.load(value)
        l.save()

    if (KafkaKey.UPDATE.value == key):
        l = Book.objects(id=int(value["id"])).first()
        l.update(**value)


def manage_review(key, value):
    if (KafkaKey.DELETE.value == key):
        return Review.objects(id=int(value["id"])).first().delete()

    # create customer property
    customer = User.objects(id=int(value["user_id"])).first()
    if customer:
        value["customer"] = user_schema.dump(customer)
    del value["user_id"]

    if (KafkaKey.CREATE.value == key):
        l = review_schema.load(value)
        l.save()

    if (KafkaKey.UPDATE.value == key):
        review = Review.objects(id=int(value["id"])).first()
        review.update(**value)


def manage_reservation(key, value):
    if (KafkaKey.DELETE.value == key):
        reservation = Reservation.objects(id=int(value["id"]))
        reservation.update(state=ReservationState.CLOSED.value)

    if (KafkaKey.CREATE.value == key):
        # create customer property
        customer = User.objects(id=int(value["customer_id"])).first()
        if customer:
            value["customer"] = user_schema.dump(customer)
        del value["customer_id"]

        # create book_copy property
        book_copy = BookCopy.objects(id=int(value["book_copy_id"])).first()
        if book_copy:
            value["book_copy"] = book_copy_schema.dump(book_copy)
            value["book_copy"]["location_id"] = value["book_copy"]["location"]["id"]
            del value["book_copy"]["location"]
        del value["book_copy_id"]

        reservation = reservation_schema.load(value)
        reservation.save()


def manage_borrowal(key, value):
    if (KafkaKey.CREATE.value == key):
        # create customer property
        customer = User.objects(id=int(value["customer_id"])).first()
        if customer:
            value["customer"] = user_schema.dump(customer)
        del value["customer_id"]

        # create employee property
        employee = User.objects(id=int(value["employee_id"])).first()
        if employee:
            value["employee"] = user_schema.dump(employee)
        del value["employee_id"]

        # create book_copy property
        book_copy = BookCopy.objects(id=int(value["book_copy_id"])).first()
        if book_copy:
            value["book_copy"] = book_copy_schema.dump(book_copy)
            value["book_copy"]["location_id"] = value["book_copy"]["location"]["id"]
            del value["book_copy"]["location"]
        del value["book_copy_id"]

        # save the borrowal
        b = borrowal_schema.load(value)
        b.save()

    if (KafkaKey.DELETE.value == key):
        b = Borrowal.objects(id=int(value["id"]))
        b.update(state=BorrowalState.RETURNED.value)


def manage_user(key, value):
    del value["password"]
    del value["reservations"]
    del value["borrowals"]
    del value["reviews"]

    if (KafkaKey.CREATE.value == key):
        u = user_schema.load(value)
        u.save()
    if (KafkaKey.UPDATE.value == key):
        u = User.objects(id=int(value["id"])).first()
        u.update(**value)


func_dict = {
    KafkaTopic.AUTHOR.value: manage_author,
    KafkaTopic.CATEGORY.value: manage_category,
    KafkaTopic.LOCATION.value: manage_location,
    KafkaTopic.BOOKCOPY.value: manage_book_copy,
    KafkaTopic.BOOK.value: manage_book,
    KafkaTopic.REVIEW.value: manage_review,
    KafkaTopic.RESERVATION.value: manage_reservation,
    KafkaTopic.BORROWAL.value: manage_borrowal,
    KafkaTopic.USER.value: manage_user,
}


def _signal_handler(signum: int, frame) -> None:
    print('Received interrupt, exiting...')
    sys.exit(0)


def run_consumer() -> None:
    print("Connecting to mongo database...")
    me.connect(
        host=f"mongodb://{MONGODB_HOSTNAME}:{MONGODB_PORT}/{MONGODB_DATABASE}",
        username=MONGODB_USERNAME, password=MONGODB_PASSWORD, authentication_source="admin"
    )

    print("Running Kafka consumer...")
    consumer = KafkaConsumer(
        "pdb",
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        key_deserializer=lambda x: x.decode(),
        value_deserializer=lambda x: loads(x.decode("utf-8")),
        api_version=(0, 10, 2)
    )

    signal.signal(signal.SIGINT, _signal_handler)

    # Wait for Kafka to initialize
    # we just poll for the topics and wait for them to be non-empty
    # we can do this, since we know the topics are created during producer initialization
    RETRY_DELAY = 3
    wait_time = 0
    while not consumer.topics():
        print(f"Waiting for Kafka to initialize {wait_time}s.")
        wait_time += RETRY_DELAY
        sleep(RETRY_DELAY)

    print("Subscribing to topics...")
    consumer.subscribe([t.value for t in KafkaTopic])

    print("Listening for messages...")
    for msg in consumer:
        topic = msg.topic
        key = msg.key
        value = msg.value
        print(f'{topic=}\t{key=}\t{value=}')

        # call function specified by topic name
        func_dict[msg.topic](key, value)


if __name__ == '__main__':
    run_consumer()
