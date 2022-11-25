from enum import Enum


class KafkaKey(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class KafkaTopic(str, Enum):
    AUTHOR = "author"
    BOOK = "book"
    BOOKCOPY = "book_copy"
    BORROWAL = "borrowal"
    CATEGORY = "category"
    LOCATION = "location"
    RESERVATION = "reservation"
    REVIEW = "review"
    USER = "user"
