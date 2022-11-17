
import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
import sqlalchemy.dialects.mysql as samysql

MYSQL_DEFAULT_PORT = 3306

Base = declarative_base()

# connection tables

Book_Author = sa.Table(
	'Book_Author',
	Base.metadata,
	sa.Column('Bookid', sa.Integer(), sa.ForeignKey('book.id'), primary_key=True),
	sa.Column('Authorid', sa.Integer(), sa.ForeignKey('author.id'), primary_key=True)
)

Book_Category = sa.Table(
	'Book_Category',
	Base.metadata,
	sa.Column('Bookid', sa.Integer(), sa.ForeignKey('book.id'), primary_key=True),
	sa.Column('Categoryid', sa.Integer(), sa.ForeignKey('category.id'), primary_key=True)
)

# entities

class SQLAuthor(Base):
	__tablename__ = 'author'

	id = sa.Column(sa.Integer(), primary_key=True)
	first_name = sa.Column(sa.VARCHAR(length=255))
	last_name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	description = sa.Column(sa.VARCHAR(length=255))

	books = relationship('Book', secondary=Book_Author, back_populates='authors')

class Category(Base):
	__tablename__ = 'category'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	description = sa.Column(sa.Text())

	books = relationship('Book', secondary=Book_Category, back_populates='categories')

class Location(Base):
	__tablename__ = 'location'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	address = sa.Column(sa.VARCHAR(length=255))

class Borrowal(Base):
	__tablename__ = 'borrowal'

	id = sa.Column(sa.Integer(), primary_key=True)
	book_copy_id = sa.Column(sa.Integer(), sa.ForeignKey('book_copy.id'), nullable=False)
	customer_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), nullable=False)
	start_date = sa.Column(sa.Date(), nullable=False)
	end_date = sa.Column(sa.Date())
	returned_date = sa.Column(sa.Date())
	state = sa.Column(samysql.TINYINT(display_width=3), nullable=False, default=0)

class BookCopy(Base):
	__tablename__ = 'book_copy'

	id = sa.Column(sa.Integer(), primary_key=True)
	book_id = sa.Column(sa.Integer(), sa.ForeignKey('book.id'), nullable=False)
	location_id = sa.Column(sa.Integer(), sa.ForeignKey('location.id'), nullable=False)
	print_date = sa.Column(sa.Date(), nullable=False)
	note = sa.Column(sa.VARCHAR(length=255))
	state = sa.Column(samysql.TINYINT(display_width=3), nullable=False, default=0)

	borrowals = relationship('Borrowal')

class User(Base):
	__tablename__ = 'user'

	id = sa.Column(sa.Integer(), primary_key=True)
	first_name = sa.Column(sa.VARCHAR(length=255))
	last_name = sa.Column(sa.VARCHAR(length=255))
	role = sa.Column(sa.VARCHAR(length=255), nullable=False)
	email = sa.Column(sa.VARCHAR(length=255), nullable=False, unique=True)
	password = sa.Column(sa.VARCHAR(length=255), nullable=False)

	reviews = relationship('Review')
	reservations = relationship('Reservation')
	borrowals = relationship('Borrowal')

class Reservation(Base):
	__tablename__ = 'reservation'

	id = sa.Column(sa.Integer(), primary_key=True)
	book_copy_id = sa.Column(sa.Integer(), sa.ForeignKey('book_copy.id'), nullable=False)
	customer_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), nullable=False)
	start_date = sa.Column(sa.Date(), nullable=False)
	end_date = sa.Column(sa.Date(), nullable=False)
	state = sa.Column(samysql.TINYINT(display_width=3), nullable=False, default=0)

class Review(Base):
	__tablename__ = 'review'

	id = sa.Column(sa.Integer(), primary_key=True)
	user_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), nullable=False)
	book_id = sa.Column(sa.Integer(), sa.ForeignKey('book.id'), nullable=False)
	title = sa.Column(sa.VARCHAR(length=255), nullable=False)
	content = sa.Column(sa.VARCHAR(length=1000))
	rating = sa.Column(sa.Integer(), nullable=False)

class Book(Base):
	__tablename__ = 'book'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	isbn = sa.Column(sa.VARCHAR(length=255), nullable=False, unique=True)
	release_date = sa.Column(sa.Date())
	description = sa.Column(sa.VARCHAR(length=1000))

	copies = relationship('BookCopy')
	reviews = relationship('Review')
	authors = relationship('SQLAuthor', secondary=Book_Author, back_populates='books')
	categories = relationship('Category', secondary=Book_Category, back_populates='books')

def sql_init(host: str = 'localhost', port: int = MYSQL_DEFAULT_PORT, username: str = 'pdb', password: str = 'pdb', echo: bool = False) -> Session:
	engine = sa.create_engine('mysql+mysqlconnector://%s:%s@%s:%d/pdb' % (username, password, host, port), echo=echo)
	Session = sessionmaker(engine)
	session = Session()
	Base.metadata.create_all(engine) # create tables

	return session
