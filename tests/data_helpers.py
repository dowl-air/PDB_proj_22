
from typing import List

from app.entity.nosql import (
    Location, Category, Author, Book, BookCopy, User, Borrowal, Reservation, Review,
    EmbeddedCategory, EmbeddedBook, EmbeddedLocation, EmbeddedBookCopy, AuthorName, EmbeddedUser
)
from app.entity.sql import (
    Location as SQLLocation, Category as SQLCategory, Author as SQLAuthor,
    Book as SQLBook, BookCopy as SQLBookCopy, User as SQLUser, Borrowal as SQLBorrowal,
    Reservation as SQLReservation, Review as SQLReview
)


# Mongo entity -> Embedded Mongo entity
def embed_category(category: Category) -> EmbeddedCategory:
    return EmbeddedCategory(id=category.id, name=category.name, description=category.description)

def embed_category_list(categories: List[Category]) -> List[EmbeddedCategory]:
    return [embed_category(category) for category in categories]

def embed_book(book: Book) -> EmbeddedBook:
    return EmbeddedBook(id=book.id, name=book.name, ISBN=book.ISBN, release_date=book.release_date, description=book.description)

def embed_book_list(books: List[Book]) -> List[EmbeddedBook]:
    return [embed_book(book) for book in books]

def embed_location(location: Location) -> EmbeddedLocation:
    return EmbeddedLocation(id=location.id, name=location.name, address=location.address)

def embed_location_list(locations: List[Location]) -> List[EmbeddedLocation]:
    return [embed_location(location) for location in locations]

def embed_book_copy(copy: BookCopy) -> EmbeddedBookCopy:
    ec = EmbeddedBookCopy(id=copy.id, book_id=copy.book_id, print_date=copy.print_date, note=copy.note, state=copy.state)

    if copy.location:
        ec.location_id = copy.location.id

    return ec

def embed_book_copy_list(copies: List[BookCopy]) -> List[EmbeddedBookCopy]:
    return [embed_book_copy(copy) for copy in copies]

def embed_author(author: Author) -> AuthorName:
    return AuthorName(id=author.id, first_name=author.first_name, last_name=author.last_name)

def embed_author_list(authors: List[Author]) -> List[AuthorName]:
    return [embed_author(author) for author in authors]

def embed_user(user: User) -> EmbeddedUser:
    return EmbeddedUser(id=user.id, first_name=user.first_name, last_name=user.last_name, role=user.role, email=user.email)

# Mongo -> SQL
def convert_location_to_sql(location: Location) -> SQLLocation:
    return SQLLocation(id=location.id, name=location.name, address=location.address)

def convert_location_list_to_sql(locations: List[Location]) -> List[SQLLocation]:
    return [convert_location_to_sql(location) for location in locations]

def convert_category_to_sql(category: Category) -> SQLCategory:
    return SQLCategory(id=category.id, name=category.name, description=category.description)

def convert_category_list_to_sql(categories: List[Category]) -> List[SQLCategory]:
    return [convert_category_to_sql(category) for category in categories]

def convert_author_to_sql(author: Author) -> SQLAuthor:
    return SQLAuthor(id=author.id, first_name=author.first_name, last_name=author.last_name,
        description=author.description)

def convert_author_list_to_sql(authors: List[Author]) -> List[SQLAuthor]:
    return [convert_author_to_sql(author) for author in authors]

def convert_book_to_sql(book: Book, authors: List[SQLAuthor], categories: List[SQLCategory]):
    nbook = SQLBook(id=book.id, name=book.id, ISBN=book.ISBN,
        release_date=book.release_date, description=book.description)

    author_ids = [author.id for author in book.authors]
    authors = list(filter(lambda x: x.id in author_ids, authors))
    nbook.authors = authors

    category_ids = [category.id for category in book.categories]
    categories = list(filter(lambda x: x.id in category_ids, categories))
    nbook.categories = categories

    return nbook

def convert_book_list_to_sql(books: List[Book], authors: List[SQLAuthor], categories: List[SQLCategory]) -> List[SQLBook]:
    return [convert_book_to_sql(book, authors, categories) for book in books]

def convert_book_copy_to_sql(copy: BookCopy) -> SQLBookCopy:
    return SQLBookCopy(id=copy.id, book_id=copy.book_id, location_id=copy.location['id'],
        print_date=copy.print_date, note=copy.note, state=copy.state)

def convert_book_copy_list_to_sql(copies: List[BookCopy]) -> List[SQLBookCopy]:
    return [convert_book_copy_to_sql(copy) for copy in copies]

def convert_user_to_sql(user: User) -> SQLUser:
    return SQLUser(id=user.id, first_name=user.first_name, last_name=user.last_name,
        role=user.role, email=user.email, password=user.last_name.lower())

def convert_user_list_to_sql(users: List[User]) -> List[SQLUser]:
    return [convert_user_to_sql(user) for user in users]

def convert_borrowal_to_sql(borrowal: Borrowal) -> SQLBorrowal:
    return SQLBorrowal(id=borrowal.id, book_copy_id=borrowal.book_copy['id'],
        customer_id=borrowal.customer['id'], start_date=borrowal.start_date,
        end_date=borrowal.end_date, returned_date=borrowal.returned_date,
        state=borrowal.state)

def convert_borrowal_list_to_sql(borrowals: List[Borrowal]) -> List[SQLBorrowal]:
    return [convert_borrowal_to_sql(borrowal) for borrowal in borrowals]

def convert_reservation_to_sql(reservation: Reservation) -> Reservation:
    return SQLReservation(id=reservation.id, book_copy_id=reservation.book_copy['id'],
        customer_id=reservation.customer['id'], start_date=reservation.start_date,
        end_date=reservation.end_date, state=reservation.state)

def convert_reservation_list_to_sql(reservations: List[Reservation]) -> List[SQLReservation]:
    return [convert_reservation_to_sql(reservation) for reservation in reservations]

def convert_review_to_sql(review: Review) -> SQLReview:
    return SQLReview(id=review.id, user_id=review.customer['id'], book_id=review.book_id,
        title=review.title, content=review.content, rating=review.rating)

def convert_review_list_to_sql(reviews: List[Review]) -> List[SQLReview]:
    return [convert_review_to_sql(review) for review in reviews]
