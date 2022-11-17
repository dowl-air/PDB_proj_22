
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base

from .associative_table import Book_Author

class Author(Base):
	__tablename__ = 'author'

	id = sa.Column(sa.Integer(), primary_key=True)
	first_name = sa.Column(sa.VARCHAR(length=255))
	last_name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	description = sa.Column(sa.VARCHAR(length=255))

	books = relationship('Book', secondary=Book_Author, back_populates='authors')
