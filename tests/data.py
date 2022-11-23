
from datetime import date, timedelta

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

# TODO
BOOK_COPY_STATE_DELETED = 0
BOOK_COPY_STATE_GOOD = 1
BOOK_COPY_STATE_DAMAGED = 2
BOOK_COPY_STATE_NEW = 3

USER_ROLE_CUSTOMER = 'customer'
USER_ROLE_EMPLOYEE = 'employee'
USER_ROLE_ADMIN = 'admin'

BORROWAL_STATE_ACTIVE = 1
BORROWAL_STATE_RETURNED = 0
BORROWAL_STATE_LOST = 2

RESERVATION_STATE_ACTIVE = 1
RESERVATION_STATE_CLOSED = 0
##

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

def embed_author(author: Author) -> AuthorName:
	return AuthorName(id=author.id, first_name=author.first_name, last_name=author.last_name)

def embed_author_list(authors: List[Author]) -> List[AuthorName]:
	return [embed_author(author) for author in authors]

def embed_book_copy_list(copies: List[BookCopy]) -> List[EmbeddedBookCopy]:
	return [embed_book_copy(copy) for copy in copies]

def embed_user(user: User) -> EmbeddedUser:
	return EmbeddedUser(id=user.id, first_name=user.first_name, last_name=user.last_name, role=user.role, email=user.email)

location_Brno = Location(id=1, name='Brno', address='Kobližná 4, 602 00 Brno-střed')
location_London = Location(id=2, name='London', address="14 St James's Square, St. James's, London SW1Y 4LG, UK")
location_Olomouc = Location(id=3, name='Olomouc', address='nám. Republiky 856/1, 779 00 Olomouc')

category_sci_fi = Category(id=1, name='Science-fiction')
category_dystopia = Category(id=2, name='Dystopia')
category_fable = Category(id=3, name='Fable')
category_fantasy = Category(id=4, name='Fantasy')
category_satire = Category(id=5, name='Satire')
category_comedy = Category(id=6, name='Comedy')
category_history = Category(id=7, name='History')
category_non_fiction = Category(id=8, name='Non-fiction')

author_Orwell = Author(id=1, first_name='George', last_name='Orwell')
author_Huxley = Author(id=2, first_name='Aldous', last_name='Huxley')
author_Tolkien = Author(id=3, first_name='John', last_name='Tolkien')
author_Gaiman = Author(id=4, first_name='Neil', last_name='Gaiman')
author_Pratchet = Author(id=5, first_name='Terry', last_name='Pratchet')

book_1984 = Book(id=1, name='1984', ISBN='978-80-7309-808-7', release_date=date(1949, 6, 9))
book_Animal_Farm = Book(id=2, name='Animal Farm', ISBN='9780451526342', release_date=date(1945, 8, 17))
book_Brave_New_World = Book(id=3, name='Brave New World', ISBN='9780099518471', release_date=date(1932, 1, 1))
book_Hobbit = Book(id=4, name='The Hobbit', ISBN='978-80-257-0741-8', release_date=date(1937, 9, 21))
book_Good_Omens = Book(id=5, name='Good Omens', ISBN='978-0-552-13703-4', release_date=date(1990, 5, 10))

author_Orwell.books = embed_book_list([book_1984, book_Animal_Farm])
author_Huxley.books = embed_book_list([book_Brave_New_World])
author_Tolkien.books = embed_book_list([book_Hobbit])
author_Gaiman.books = embed_book_list([book_Good_Omens])
author_Pratchet.books = embed_book_list([book_Good_Omens])

book_1984.authors = embed_author_list([author_Orwell])
book_Animal_Farm.authors = embed_author_list([author_Orwell])
book_Brave_New_World.authors = embed_author_list([author_Huxley])
book_Hobbit.authors = embed_author_list([author_Tolkien])
book_Good_Omens.authors = embed_author_list([author_Gaiman, author_Pratchet])

bc_1984_Brno_1 = BookCopy(
	id=1, book_id=book_1984.id, print_date=date(2014, 10, 11), note='Slightly used',
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Brno)
)
bc_1984_Brno_2 = BookCopy(
	id=2, book_id=book_1984.id, print_date=date(2022, 1, 16),
	state=BOOK_COPY_STATE_NEW, location=embed_location(location_Brno)
)
bc_1984_London_1 = BookCopy(
	id=3, book_id=book_1984.id, print_date=date(2021, 1, 16),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_London)
)
bc_1984_London_2 = BookCopy(
	id=4, book_id=book_1984.id, print_date=date(1990, 5, 21),
	state=BOOK_COPY_STATE_DAMAGED, location=embed_location(location_London)
)
bc_1984_London_3 = BookCopy(
	id=5, book_id=book_1984.id, print_date=date(2005, 2, 22), note='Lost',
	state=BOOK_COPY_STATE_DELETED, location=embed_location(location_London)
)
bc_Animal_Farm_Brno = BookCopy(
	id=6, book_id=book_Animal_Farm.id, print_date=date(2021, 5, 8),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Brno)
)
bc_Animal_Farm_London = BookCopy(
	id=8, book_id=book_Animal_Farm.id, print_date=date(2022, 6, 13),
	state=BOOK_COPY_STATE_NEW, location=embed_location(location_Olomouc)
)
bc_Animal_Farm_Olomouc = BookCopy(
	id=9, book_id=book_Animal_Farm.id, print_date=date(2017, 6, 13),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Olomouc)
)
bc_Brave_New_World_Brno = BookCopy(
	id=10, book_id=book_Brave_New_World.id, print_date=date(2019, 8, 18),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Brno)
)
bc_Brave_New_World_London = BookCopy(
	id=11, book_id=book_Brave_New_World.id, print_date=date(2021, 6, 1),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_London)
)
bc_Hobbit_Brno = BookCopy(
	id=12, book_id=book_Hobbit.id, print_date=date(2020, 4, 8),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Brno)
)
bc_Hobbit_London_1 = BookCopy(
	id=13, book_id=book_Hobbit.id, print_date=date(2018, 11, 4),
	state=BOOK_COPY_STATE_DAMAGED, location=embed_location(location_London)
)
bc_Hobbit_London_2 = BookCopy(
	id=14, book_id=book_Hobbit.id, print_date=date(2021, 3, 11),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_London)
)
bc_Hobbit_Olomouc = BookCopy(
	id=15, book_id=book_Hobbit.id, print_date=date(2017, 10, 5),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Olomouc)
)
bc_Good_Omens_Brno = BookCopy(
	id=16, book_id=book_Good_Omens.id, print_date=date(2019, 11, 11),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(location_Brno)
)

book_1984.book_copies = embed_book_copy_list([bc_1984_Brno_1, bc_1984_Brno_2, bc_1984_London_1, bc_1984_London_2, bc_1984_London_3])
book_Animal_Farm.book_copies = embed_book_copy_list([bc_Animal_Farm_Brno, bc_Animal_Farm_London, bc_Animal_Farm_Olomouc])
book_Brave_New_World.book_copies = embed_book_copy_list([bc_Brave_New_World_Brno, bc_Brave_New_World_London])
book_Hobbit.book_copies = embed_book_copy_list([bc_Hobbit_Brno, bc_Hobbit_London_1, bc_Hobbit_London_2, bc_Hobbit_Olomouc])
book_Good_Omens.book_copies = embed_book_copy_list([bc_Good_Omens_Brno])

book_1984.categories = embed_category_list([category_sci_fi, category_dystopia])
book_Animal_Farm.categories = embed_category_list([category_fable, category_satire])
book_Brave_New_World.categories = embed_category_list([category_dystopia])
book_Hobbit.categories = embed_category_list([category_fantasy])
book_Good_Omens.categories = embed_category_list([category_fantasy, category_comedy])

user_customer_Customer = User(id=1, first_name='Customer', last_name='Customer', role=USER_ROLE_CUSTOMER, email='customer@customer.com')
user_customer_Smith = User(id=2, first_name='John', last_name='Smith', role=USER_ROLE_CUSTOMER, email='smith@customer.com')
user_customer_Reviewer = User(id=3, first_name='Joe', last_name='Reviewer', role=USER_ROLE_CUSTOMER, email='reviewer@customer.com')
user_employee_Brno = User(id=4, first_name='Employee', last_name='Brno', role=USER_ROLE_EMPLOYEE, email='brno@employee.com')
user_employee_London = User(id=5, first_name='Employee', last_name='London', role=USER_ROLE_EMPLOYEE, email='london@employee.com')
user_employee_Olomouc = User(id=6, first_name='Employee', last_name='Olomouc', role=USER_ROLE_EMPLOYEE, email='olomouc@employee.com')
user_admin_Admin = User(id=7, first_name='Admin', last_name='Admin', role=USER_ROLE_ADMIN, email='admin@admin.com')

BORROWAL_LENGTH = timedelta(days=30)
start_date = date(2019, 10, 4)
borrowal_London_1 = Borrowal(
	id=1, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 10, 24), state=BORROWAL_STATE_RETURNED,
	book_copy=embed_book_copy(bc_1984_London_1), customer=embed_user(user_customer_Customer), employee=embed_user(user_employee_London)
)
start_date = date(2018, 8, 7)
borrowal_London_2 = Borrowal(
	id=2, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, state=BORROWAL_STATE_LOST,
	book_copy=embed_book_copy(bc_1984_London_3), customer=embed_user(user_customer_Smith), employee=embed_user(user_employee_London)
)
start_date = date(2019, 11, 25)
borrowal_London_3 = Borrowal(
	id=3, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 12, 10), state=BORROWAL_STATE_RETURNED,
	book_copy=embed_book_copy(bc_Animal_Farm_London), customer=embed_user(user_customer_Customer), employee=embed_user(user_employee_London)
)
start_date = date(2019, 5, 6)
borrowal_Brno_1 = Borrowal(
	id=4, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 5, 15), state=BORROWAL_STATE_RETURNED,
	book_copy=embed_book_copy(bc_Good_Omens_Brno), customer=embed_user(user_customer_Customer), employee=embed_user(user_employee_Brno)
)
borrowal_Brno_2 = Borrowal(
	id=5, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 5, 18), state=BORROWAL_STATE_RETURNED,
	book_copy=embed_book_copy(bc_Hobbit_Brno), customer=embed_user(user_customer_Customer), employee=embed_user(user_employee_Brno)
)
start_date = date(2020, 6, 10)
borrowal_Olomouc = Borrowal(
	id=6, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2020, 6, 10), state=BORROWAL_STATE_RETURNED,
	book_copy=embed_book_copy(bc_Animal_Farm_Olomouc), customer=embed_user(user_customer_Smith), employee=embed_user(user_employee_Olomouc)
)
start_date = date(2022, 11, 20)
borrowal_Brno_active = Borrowal(
	id=7, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, state=BORROWAL_STATE_ACTIVE,
	book_copy=embed_book_copy(bc_1984_Brno_1), customer=embed_user(user_customer_Smith), employee=embed_user(user_employee_Olomouc)
)

RESERVATION_LENGTH = timedelta(days=7)
start_date = date(2022, 11, 20)
reservation_Brno = Reservation(
	id=1, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_CLOSED,
	book_copy=embed_book_copy(bc_1984_Brno_2), customer=embed_user(user_customer_Customer)
)
start_date = date(2020, 6, 6)
reservation_Olomouc = Reservation(
	id=2, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_CLOSED,
	book_copy=embed_book_copy(bc_Animal_Farm_Olomouc), customer=embed_user(user_customer_Smith)
)
start_date = date(2022, 11, 20)
reservation_Brno_active = Reservation(
	id=3, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_ACTIVE,
	book_copy=embed_book_copy(bc_Animal_Farm_Brno), customer=embed_user(user_customer_Customer)
)

review_1984 = Review(id=1, book_id=book_1984.id, title='Good book', content='I liked it', rating=9, customer=embed_user(user_customer_Reviewer))
review_Animal_Farm = Review(id=2, book_id=book_Animal_Farm.id, title='OK book', content='Four legs good, two legs bad', rating=7, customer=embed_user(user_customer_Reviewer))
review_Hobbit = Review(id=3, book_id=book_Hobbit.id, title='Better than the movie', content='OK', rating=6, customer=embed_user(user_customer_Reviewer))
review_Good_Omens_1 = Review(id=4, book_id=book_Good_Omens.id, title='Good Omens Review', content='Fun', rating=8, customer=embed_user(user_customer_Reviewer))
review_Good_Omens_2 = Review(id=5, book_id=book_Good_Omens.id, title='Liked it!', rating=9, customer=embed_user(user_customer_Customer))

LOCATIONS = [location_Brno, location_London, location_Olomouc]
CATEGORIES = [
	category_sci_fi, category_dystopia, category_fable, category_fantasy,
	category_satire, category_comedy, category_history, category_non_fiction
]
AUTHORS = [author_Orwell, author_Huxley, author_Tolkien, author_Gaiman, author_Pratchet]
BOOKS = [book_1984, book_Animal_Farm, book_Brave_New_World, book_Hobbit, book_Good_Omens]
BOOK_COPIES = [
	bc_1984_Brno_1, bc_1984_Brno_2, bc_1984_London_1, bc_1984_London_2, bc_1984_London_3, bc_Animal_Farm_Brno,
	bc_Animal_Farm_London, bc_Animal_Farm_Olomouc, bc_Brave_New_World_Brno, bc_Brave_New_World_London,
	bc_Hobbit_Brno, bc_Hobbit_London_1, bc_Hobbit_London_2, bc_Hobbit_Olomouc, bc_Good_Omens_Brno
]
USERS = [
	user_customer_Customer, user_customer_Smith, user_customer_Reviewer,
	user_employee_Brno, user_employee_London, user_employee_Olomouc,
	user_admin_Admin
]
BORROWALS = [
	borrowal_London_1, borrowal_London_2, borrowal_London_3, borrowal_Brno_1,
	borrowal_Brno_2, borrowal_Olomouc, borrowal_Brno_active
]
RESERVATIONS = [reservation_Brno, reservation_Olomouc, reservation_Brno_active]
REVIEWS = [review_1984, review_Animal_Farm, review_Hobbit, review_Good_Omens_1, review_Good_Omens_2]

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

SQL_LOCATIONS = convert_location_list_to_sql(LOCATIONS)
SQL_CATEGORIES = convert_category_list_to_sql(CATEGORIES)
SQL_AUTHORS = convert_author_list_to_sql(AUTHORS)
SQL_BOOKS = convert_book_list_to_sql(BOOKS, SQL_AUTHORS, SQL_CATEGORIES)
SQL_BOOK_COPIES = convert_book_copy_list_to_sql(BOOK_COPIES)
SQL_USERS = convert_user_list_to_sql(USERS)
SQL_BORROWALS = convert_borrowal_list_to_sql(BORROWALS)
SQL_RESERVATIONS = convert_reservation_list_to_sql(RESERVATIONS)
SQL_REVIEWS = convert_review_list_to_sql(REVIEWS)
