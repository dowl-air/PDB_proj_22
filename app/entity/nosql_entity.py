
import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import mongoengine as me

MONGO_DEFAULT_PORT = 27017

def prot_connect(host: str = 'localhost', port: int = MONGO_DEFAULT_PORT, timeout: int = 3000) -> MongoClient:
	conn: MongoClient = me.connect('pdb', serverSelectionTimeoutMS=timeout)

	try:
		conn.admin.command('ping')
	except ConnectionFailure:
		print('Failed to connect to the database server at %s:%i' % (host, port), file=sys.stderr)
		sys.exit(1)

	return conn

# helpers

class AuthorName(me.EmbeddedDocument):
	id = me.IntField(null=False)
	first_name = me.StringField()
	last_name = me.StringField()

class EmbeddedLocation(me.EmbeddedDocument):
	id = me.IntField(null=False)
	name = me.StringField()
	address = me.StringField()

class EmbeddedCategory(me.EmbeddedDocument):
	id = me.IntField(null=False)
	name = me.StringField()
	description = me.StringField()

class EmbeddedBookCopy(me.EmbeddedDocument):
	id = me.IntField(null=False)
	book_id = me.IntField()
	print_date = me.DateField()
	note = me.StringField()
	state = me.IntField()
	location_id = me.IntField()

class EmbeddedUser(me.EmbeddedDocument):
	id = me.IntField(null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	role = me.StringField()
	email = me.StringField()

class EmbeddedBook(me.EmbeddedDocument):
	id = me.IntField(primary_key=True, null=False)
	name = me.StringField()
	isbn = me.StringField()
	release_date = me.DateField()
	description = me.StringField()

# entities

class Location(me.Document):
	id = me.IntField(primary_key=True, null=False)
	name = me.StringField()
	address = me.StringField()

class Category(me.Document):
	id = me.IntField(primary_key=True, null=False)
	name = me.StringField()
	description = me.StringField()

class BookCopy(me.Document):
	id = me.IntField(primary_key=True, null=False)
	book_id = me.IntField()
	print_date = me.DateField()
	note = me.StringField()
	state = me.IntField()
	location = me.EmbeddedDocumentField(EmbeddedLocation)

class Book(me.Document):
	id = me.IntField(primary_key=True, null=False)
	authors = me.EmbeddedDocumentListField(AuthorName)
	name = me.StringField()
	isbn = me.StringField()
	release_date = me.DateField()
	description = me.StringField()
	book_copies = me.EmbeddedDocumentListField(EmbeddedBookCopy)
	categories = me.EmbeddedDocumentListField(EmbeddedCategory)

class User(me.Document):
	id = me.IntField(primary_key=True, null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	role = me.StringField()
	email = me.StringField()

class Borrowal(me.Document):
	id = me.IntField(primary_key=True, null=False)
	borrowed_date = me.DateField()
	start_date = me.DateField()
	end_date = me.DateField()
	returned_date = me.DateField()
	state = me.IntField()
	book_copy = me.EmbeddedDocumentField(EmbeddedBookCopy)
	customer = me.EmbeddedDocumentField(EmbeddedUser)
	employee = me.EmbeddedDocumentField(EmbeddedUser)

class Review(me.Document):
	id = me.IntField(primary_key=True, null=False)
	book_id = me.IntField()
	title = me.StringField()
	content = me.StringField()
	rating = me.IntField()
	customer = me.EmbeddedDocumentField(EmbeddedUser)

class Author(me.Document):
	id = me.IntField(primary_key=True, null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	description = me.StringField()
	books = me.EmbeddedDocumentListField(EmbeddedBook)

class Reservation(me.Document):
	id = me.IntField(primary_key=True, null=False)
	start_date = me.DateField()
	end_date = me.DateField()
	state = me.IntField()
	book_copy = me.EmbeddedDocumentField(EmbeddedBookCopy)
	customer = me.EmbeddedDocumentField(EmbeddedUser)
