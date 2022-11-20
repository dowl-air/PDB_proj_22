
import pytest
from datetime import date, timedelta

from typing import List

from app.create_app import create_app, db, mongo

from app.entity.nosql import (
	Location, Category, Author, Book, BookCopy, User, Borrowal, Reservation, Review,
	EmbeddedCategory, EmbeddedBook, EmbeddedLocation, EmbeddedBookCopy, AuthorName, EmbeddedUser
)

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

@pytest.fixture(scope='session', autouse=True)
def clear_db():
	with create_app().app_context():
		db.drop_all()
		mongo.connection['default'].drop_database('pdb')

@pytest.fixture
def client():
	with create_app().test_client() as client:
		yield client

locationBrno = Location(id=1, name='Brno', address='Kobližná 4, 602 00 Brno-střed')
locationLondon = Location(id=2, name='London', address="14 St James's Square, St. James's, London SW1Y 4LG, UK")
locationOlomouc = Location(id=3, name='Olomouc', address='nám. Republiky 856/1, 779 00 Olomouc')

categorySciFi = Category(id=1, name='Science-fiction')
categoryDystopia = Category(id=2, name='Dystopia')
categoryFable = Category(id=3, name='Fable')
categoryFantasy = Category(id=4, name='Fantasy')
categorySatire = Category(id=5, name='Satire')
categoryComedy = Category(id=6, name='Comedy')

authorOrwell = Author(id=1, first_name='George', last_name='Orwell')
authorHuxley = Author(id=2, first_name='Aldous', last_name='Huxley')
authorTolkien = Author(id=3, first_name='John', last_name='Tolkien')
authorGaiman = Author(id=4, first_name='Neil', last_name='Gaiman')
authorPratchet = Author(id=5, first_name='Terry', last_name='Pratchet')

book1984 = Book(id=1, name='1984', ISBN='978-80-7309-808-7', release_date=date(1949, 6, 9))
bookAnimalFarm = Book(id=2, name='Animal Farm', ISBN='9780451526342', release_date=date(1945, 8, 17))
bookBraveNewWorld = Book(id=3, name='Brave New World', ISBN='9780099518471', release_date=date(1932, 1, 1))
bookHobbit = Book(id=4, name='The Hobbit', ISBN='978-80-257-0741-8', release_date=date(1937, 9, 21))
bookGoodOmens = Book(id=5, name='Good Omens', ISBN='978-0-552-13703-4', release_date=date(1990, 5, 10))

authorOrwell.books = embed_book_list([book1984, bookAnimalFarm]) # TODO
authorHuxley.books = embed_book_list([bookBraveNewWorld])
authorTolkien.books = embed_book_list([bookHobbit])
authorGaiman.books = embed_book_list([bookGoodOmens])
authorPratchet.books = embed_book_list([bookGoodOmens])

book1984.authors = embed_author_list([authorOrwell])
bookAnimalFarm.authors = embed_author_list([authorOrwell])
bookBraveNewWorld.authors = embed_author_list([authorHuxley])
bookHobbit.authors = embed_author_list([authorTolkien])
bookGoodOmens.authors = embed_author_list([authorGaiman, authorPratchet])

bc1984Brno1 = BookCopy(id=1, book_id=book1984.id, print_date=date(2014, 10, 11), note='Slightly used',
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationBrno))
bc1984Brno2 = BookCopy(id=2, book_id=book1984.id, print_date=date(2022, 1, 16),
	state=BOOK_COPY_STATE_NEW, location=embed_location(locationBrno))
bc1984London1 = BookCopy(id=3, book_id=book1984.id, print_date=date(2021, 1, 16),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationLondon))
bc1984London2 = BookCopy(id=4, book_id=book1984.id, print_date=date(1990, 5, 21),
	state=BOOK_COPY_STATE_DAMAGED, location=embed_location(locationLondon))
bc1984London3 = BookCopy(id=5, book_id=book1984.id, print_date=date(2005, 2, 22), note='Lost',
	state=BOOK_COPY_STATE_DELETED, location=embed_location(locationLondon))
bcAnimalFarmBrno = BookCopy(id=6, book_id=bookAnimalFarm.id,
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationBrno))
bcAnimalFarmLondon = BookCopy(id=8, book_id=bookAnimalFarm.id, print_date=date(2022, 6, 13),
	state=BOOK_COPY_STATE_NEW, location=embed_location(locationOlomouc))
bcAnimalFarmOlomouc = BookCopy(id=9, book_id=bookAnimalFarm.id, print_date=date(2017, 6, 13),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationOlomouc))
bcBraveNewWorldBrno = BookCopy(id=10, book_id=bookBraveNewWorld.id, print_date=date(2019, 8, 18),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationBrno))
bcBraveNewWorldLondon = BookCopy(id=11, book_id=bookBraveNewWorld.id,
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationLondon))
bcHobbitBrno = BookCopy(id=12, book_id=bookHobbit.id, print_date=date(2020, 4, 8),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationBrno))
bcHobbitLondon1 = BookCopy(id=13, book_id=bookHobbit.id,
	state=BOOK_COPY_STATE_DAMAGED, location=embed_location(locationLondon))
bcHobbitLondon2 = BookCopy(id=14, book_id=bookHobbit.id, print_date=date(2021, 3, 11),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationLondon))
bcHobbitOlomouc = BookCopy(id=15, book_id=bookHobbit.id, print_date=date(2017, 10, 5),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationOlomouc))
bcGoodOmensBrno = BookCopy(id=16, book_id=bookGoodOmens.id, print_date=date(2019, 11, 11),
	state=BOOK_COPY_STATE_GOOD, location=embed_location(locationBrno))

book1984.book_copies = embed_book_copy_list([bc1984Brno1, bc1984Brno2, bc1984London1, bc1984London2, bc1984London3])
bookAnimalFarm.book_copies = embed_book_copy_list([bcAnimalFarmBrno, bcAnimalFarmLondon, bcAnimalFarmOlomouc])
bookBraveNewWorld.book_copies = embed_book_copy_list([bcBraveNewWorldBrno, bcBraveNewWorldLondon])
bookHobbit.book_copies = embed_book_copy_list([bcHobbitBrno, bcHobbitLondon1, bcHobbitLondon2, bcHobbitOlomouc])
bookGoodOmens.book_copies = embed_book_copy_list([bcGoodOmensBrno])

book1984.categories = embed_category_list([categorySciFi, categoryDystopia])
bookAnimalFarm.categories = embed_category_list([categoryFable, categorySatire])
bookBraveNewWorld.categories = embed_category_list([categoryDystopia])
bookHobbit.categories = embed_category_list([categoryFantasy])
bookGoodOmens.categories = embed_category_list([categoryFantasy, categoryComedy])

userCustomerCustomer = User(id=1, first_name='Customer', last_name='Customer', role=USER_ROLE_CUSTOMER, email='customer@customer.com')
userCustomerSmith = User(id=2, first_name='John', last_name='Smith', role=USER_ROLE_CUSTOMER, email='smith@customer.com')
userCustomerReviewer = User(id=3, first_name='Joe', last_name='Reviewer', role=USER_ROLE_CUSTOMER, email='reviewer@customer.com')
userEmployeeBrno = User(id=4, first_name='Employee', last_name='Brno', role=USER_ROLE_EMPLOYEE, email='brno@employee.com')
userEmployeeLondon = User(id=5, first_name='Employee', last_name='London', role=USER_ROLE_EMPLOYEE, email='london@employee.com')
userEmployeeOlomouc = User(id=6, first_name='Employee', last_name='Olomouc', role=USER_ROLE_EMPLOYEE, email='olomouc@employee.com')
userAdmin = User(id=7, first_name='Admin', last_name='Admin', role=USER_ROLE_ADMIN, email='admin@admin.com')

start_date = date(2019, 10, 4)
BORROWAL_LENGTH = timedelta(days=30)
borrowalLondon1 = Borrowal(id=1, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 10, 24),
	state=BORROWAL_STATE_RETURNED, book_copy=embed_book_copy(bc1984London1), customer=embed_user(userCustomerCustomer), employee=embed_user(userEmployeeLondon))
start_date = date(2018, 8, 7)
borrowalLondon2 = Borrowal(id=2, start_date=start_date, end_date=start_date + BORROWAL_LENGTH,
	state=BORROWAL_STATE_LOST, book_copy=embed_book_copy(bc1984London3), customer=embed_user(userCustomerSmith), employee=embed_user(userEmployeeLondon))
start_date = date(2019, 11, 25)
borrowalLondon3 = Borrowal(id=3, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 12, 10),
	state=BORROWAL_STATE_RETURNED, book_copy=embed_book_copy(bcAnimalFarmLondon), customer=embed_user(userCustomerCustomer), employee=embed_user(userEmployeeLondon))
start_date = date(2019, 5, 6)
borrowalBrno1 = Borrowal(id=4, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 5, 15),
	state=BORROWAL_STATE_RETURNED, book_copy=embed_book_copy(bcGoodOmensBrno), customer=embed_user(userCustomerCustomer), employee=embed_user(userEmployeeBrno))
borrowalBrno2 = Borrowal(id=5, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2019, 5, 18),
	state=BORROWAL_STATE_RETURNED, book_copy=embed_book_copy(bcHobbitBrno), customer=embed_user(userCustomerCustomer), employee=embed_user(userEmployeeBrno))
start_date = date(2020, 6, 10)
borrowalOlomouc = Borrowal(id=6, start_date=start_date, end_date=start_date + BORROWAL_LENGTH, returned_date=date(2020, 6, 10),
	state=BORROWAL_STATE_RETURNED, book_copy=embed_book_copy(bcAnimalFarmOlomouc), customer=embed_user(userCustomerSmith), employee=embed_user(userEmployeeOlomouc))
start_date = date(2022, 11, 20)
borrowalBrnoActive1 = Borrowal(id=7, start_date=start_date, end_date=start_date + BORROWAL_LENGTH,
	state=BORROWAL_STATE_ACTIVE, book_copy=embed_book_copy(bc1984Brno1), customer=embed_user(userCustomerSmith), employee=embed_user(userEmployeeOlomouc))

start_date = date(2022, 11, 20)
RESERVATION_LENGTH = timedelta(days=7)
reservationBrno = Reservation(id=1, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_CLOSED,
	book_copy=embed_book_copy(bc1984Brno2), customer=embed_user(userCustomerCustomer))
start_date = date(2020, 6, 6)
reservationOlomouc = Reservation(id=2, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_CLOSED,
	book_copy=embed_book_copy(bcAnimalFarmOlomouc), customer=embed_user(userCustomerSmith))
start_date = date(2022, 11, 20)
reservationBrnoActive = Reservation(id=3, start_date=start_date, end_date=start_date + RESERVATION_LENGTH, state=RESERVATION_STATE_ACTIVE,
	book_copy=embed_book_copy(bcAnimalFarmBrno), customer=embed_user(userCustomerCustomer))

review1984 = Review(id=1, book_id=book1984.id, title='Good book', content='I liked it', rating=9, customer=embed_user(userCustomerReviewer))
reviewAnimalFarm = Review(id=2, book_id=bookAnimalFarm.id, title='OK book', content='Four legs good, two legs bad', rating=7, customer=embed_user(userCustomerReviewer))
reviewHobbit = Review(id=3, book_id=bookHobbit.id, title='Better than the movie', content='OK', rating=6, customer=embed_user(userCustomerReviewer))
reviewGoodOmens1 = Review(id=4, book_id=bookGoodOmens.id, title='Good Omens Review', content='Fun', rating=8, customer=embed_user(userCustomerReviewer))
reviewGoodOmens2 = Review(id=5, book_id=bookGoodOmens.id, title='Liked it!', rating=9, customer=embed_user(userCustomerCustomer))

LOCATIONS = [locationBrno, locationLondon, locationOlomouc]
CATEGORIES = [categorySciFi, categoryDystopia, categoryFable, categoryFantasy, categorySatire, categoryComedy]
AUTHORS = [authorOrwell, authorHuxley, authorTolkien, authorGaiman, authorPratchet]
BOOKS = [book1984, bookAnimalFarm, bookBraveNewWorld, bookHobbit, bookGoodOmens]
BOOK_COPIES = [bc1984Brno1, bc1984Brno2, bc1984London1, bc1984London2, bc1984London3,
	bcAnimalFarmBrno, bcAnimalFarmLondon, bcAnimalFarmOlomouc, bcBraveNewWorldBrno, bcBraveNewWorldLondon,
	bcHobbitBrno, bcHobbitLondon1, bcHobbitLondon2, bcHobbitOlomouc, bcGoodOmensBrno]
USERS = [userCustomerCustomer, userCustomerSmith, userCustomerReviewer,
	userEmployeeBrno, userEmployeeLondon, userEmployeeOlomouc,
	userAdmin]
BORROWALS = [borrowalLondon1, borrowalLondon2, borrowalLondon3, borrowalBrno1, borrowalBrno2, borrowalOlomouc, borrowalBrnoActive1]
RESERVATIONS = [reservationBrno, reservationOlomouc, reservationBrnoActive]
REVIEWS = [review1984, reviewAnimalFarm, reviewHobbit, reviewGoodOmens1, reviewGoodOmens2]

@pytest.fixture(scope='session', autouse=True)
def fill_db():
	with create_app().app_context():
		for arr in [LOCATIONS, CATEGORIES, AUTHORS, BOOKS, BOOK_COPIES, USERS, BORROWALS, RESERVATIONS]:
			for it in arr:
				it.save()
