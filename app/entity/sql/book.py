
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base

from .associative_table import Book_Author, Book_Category

class Book(Base):
	__tablename__ = 'book'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	ISBN = sa.Column(sa.VARCHAR(length=255), nullable=False, unique=True)
	release_date = sa.Column(sa.Date())
	description = sa.Column(sa.VARCHAR(length=1000))

	copies = relationship('BookCopy')
	reviews = relationship('Review')
	authors = relationship('Author', secondary=Book_Author, back_populates='books')
	categories = relationship('Category', secondary=Book_Category, back_populates='books')
