
import os
from datetime import date, timedelta

from app.create_app import create_app, db, mongo
from app.entity.nosql import (
	Location, Category, Author, Book, BookCopy, User, Borrowal, Reservation, Review
)
from app.entity import UserRole

from data_helpers import (
	embed_book_list, embed_author_list, embed_book_copy_list, embed_category_list,
	embed_location, embed_book_copy, embed_user,

	convert_location_list_to_sql, convert_author_list_to_sql, convert_category_list_to_sql,
	convert_book_list_to_sql, convert_book_copy_list_to_sql, convert_user_list_to_sql,
	convert_borrowal_list_to_sql, convert_reservation_list_to_sql, convert_review_list_to_sql
)

# TODO
BOOK_COPY_STATE_DELETED = 0
BOOK_COPY_STATE_GOOD = 1
BOOK_COPY_STATE_DAMAGED = 2
BOOK_COPY_STATE_NEW = 3

BORROWAL_STATE_ACTIVE = 1
BORROWAL_STATE_RETURNED = 0
BORROWAL_STATE_LOST = 2

RESERVATION_STATE_ACTIVE = 1
RESERVATION_STATE_CLOSED = 0
##

BORROWAL_LENGTH = timedelta(days=30)
RESERVATION_LENGTH = timedelta(days=7)

# LOCATIONS
location_Brno = Location(id=1, name='Brno', address='Kobližná 4, 602 00 Brno-střed')
location_London = Location(id=2, name='London', address="14 St James's Square, St. James's, London SW1Y 4LG, UK")
location_Olomouc = Location(id=3, name='Olomouc', address='nám. Republiky 856/1, 779 00 Olomouc')

# CATEGORIES
category_sci_fi = Category(id=1, name='Science-fiction')
category_dystopia = Category(id=2, name='Dystopia')
category_fable = Category(id=3, name='Fable')
category_fantasy = Category(id=4, name='Fantasy')
category_satire = Category(id=5, name='Satire')
category_comedy = Category(id=6, name='Comedy')
category_history = Category(id=7, name='History')
category_non_fiction = Category(id=8, name='Non-fiction')

# AUTHORS
author_Orwell = Author(id=1, first_name='George', last_name='Orwell')
author_Huxley = Author(id=2, first_name='Aldous', last_name='Huxley')
author_Tolkien = Author(id=3, first_name='John', last_name='Tolkien')
author_Gaiman = Author(id=4, first_name='Neil', last_name='Gaiman')
author_Pratchet = Author(id=5, first_name='Terry', last_name='Pratchet')

# BOOKS
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

# BOOK COPIES
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

# USERS
user_customer_Customer = User(id=1, first_name='Customer', last_name='Customer', role=UserRole.CUSTOMER, email='customer@customer.com')
user_customer_Smith = User(id=2, first_name='John', last_name='Smith', role=UserRole.CUSTOMER, email='smith@customer.com')
user_customer_Reviewer = User(id=3, first_name='Joe', last_name='Reviewer', role=UserRole.CUSTOMER, email='reviewer@customer.com')
user_employee_Brno = User(id=4, first_name='Employee', last_name='Brno', role=UserRole.EMPLOYEE, email='brno@employee.com')
user_employee_London = User(id=5, first_name='Employee', last_name='London', role=UserRole.EMPLOYEE, email='london@employee.com')
user_employee_Olomouc = User(id=6, first_name='Employee', last_name='Olomouc', role=UserRole.EMPLOYEE, email='olomouc@employee.com')
user_admin_Admin = User(id=7, first_name='Admin', last_name='Admin', role=UserRole.ADMIN, email='admin@admin.com')

# BORROWALS
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
start_date = date.today()
borrowal_Brno_active = Borrowal(
	id=7, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, state=BORROWAL_STATE_ACTIVE,
	book_copy=embed_book_copy(bc_1984_Brno_1), customer=embed_user(user_customer_Smith), employee=embed_user(user_employee_Olomouc)
)
start_date = date(2020, 11, 6)
borrowal_Olomouc_active = Borrowal(
	id=8, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, state=BORROWAL_STATE_ACTIVE, # expired
	book_copy=embed_book_copy(bc_Brave_New_World_Brno), customer=embed_user(user_customer_Smith), employee=embed_user(user_employee_Brno)
)

# RESERVATIONS
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
start_date = date.today()
reservation_Brno_active = Reservation(
	id=3, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_ACTIVE,
	book_copy=embed_book_copy(bc_Animal_Farm_Brno), customer=embed_user(user_customer_Customer)
)
start_date = date(2021, 4, 6)
reservation_London_active_1 = Reservation(
	id=4, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_ACTIVE, # expired
	book_copy=embed_book_copy(bc_Hobbit_London_1), customer=embed_user(user_customer_Smith)
)
start_date = date.today()
reservation_London_active_2 = Reservation(
	id=5, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_ACTIVE,
	book_copy=embed_book_copy(bc_Hobbit_London_2), customer=embed_user(user_customer_Smith)
)

# REVIEWS
review_1984 = Review(
	id=1, book_id=book_1984.id, title='Good book', content='I liked it',
	rating=9, customer=embed_user(user_customer_Reviewer)
)
review_Animal_Farm = Review(
	id=2, book_id=book_Animal_Farm.id, title='OK book', content='Four legs good, two legs bad',
	rating=7, customer=embed_user(user_customer_Reviewer)
)
review_Hobbit = Review(
	id=3, book_id=book_Hobbit.id, title='Better than the movie', content='OK',
	rating=6, customer=embed_user(user_customer_Reviewer)
)
review_Good_Omens_1 = Review(
	id=4, book_id=book_Good_Omens.id, title='Good Omens Review', content='Fun',
	rating=8, customer=embed_user(user_customer_Reviewer)
)
review_Good_Omens_2 = Review(
	id=5, book_id=book_Good_Omens.id, title='Liked it!',
	rating=9, customer=embed_user(user_customer_Customer)
)

# lists of Mongo entities 
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
	borrowal_Brno_2, borrowal_Olomouc, borrowal_Brno_active, borrowal_Olomouc_active
]
RESERVATIONS = [reservation_Brno, reservation_Olomouc, reservation_Brno_active, reservation_London_active_1, reservation_London_active_2]
REVIEWS = [review_1984, review_Animal_Farm, review_Hobbit, review_Good_Omens_1, review_Good_Omens_2]

# SQL versions of Mongo entities
SQL_LOCATIONS = convert_location_list_to_sql(LOCATIONS)
SQL_CATEGORIES = convert_category_list_to_sql(CATEGORIES)
SQL_AUTHORS = convert_author_list_to_sql(AUTHORS)
SQL_BOOKS = convert_book_list_to_sql(BOOKS, SQL_AUTHORS, SQL_CATEGORIES)
SQL_BOOK_COPIES = convert_book_copy_list_to_sql(BOOK_COPIES)
SQL_USERS = convert_user_list_to_sql(USERS)
SQL_BORROWALS = convert_borrowal_list_to_sql(BORROWALS)
SQL_RESERVATIONS = convert_reservation_list_to_sql(RESERVATIONS)
SQL_REVIEWS = convert_review_list_to_sql(REVIEWS)

# removes all data from both databases
def clear_db() -> None:
	MONGO_DB_NAME = os.getenv('MONGODB_DATABASE', 'pdb')

	with create_app().app_context():
		db.drop_all()
		mongo.connection['default'].drop_database(MONGO_DB_NAME)

# fills both databases with test data
def fill_db() -> None:
	with create_app().app_context():
		for arr in [LOCATIONS, CATEGORIES, AUTHORS, BOOKS, BOOK_COPIES, USERS, BORROWALS, RESERVATIONS, REVIEWS]:
			for it in arr:
				it.save()

		db.create_all()
		for arr in [SQL_LOCATIONS, SQL_CATEGORIES, SQL_AUTHORS, SQL_BOOKS, SQL_BOOK_COPIES, SQL_USERS, SQL_BORROWALS, SQL_RESERVATIONS, SQL_REVIEWS]:
			for it in arr:
				db.session.add(it)
			db.session.commit()

if __name__ == '__main__':
	clear_db()
	fill_db()
