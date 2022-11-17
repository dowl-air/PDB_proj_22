
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base

from .associative_table import Book_Category

class Category(Base):
	__tablename__ = 'category'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	description = sa.Column(sa.Text())

	books = relationship('Book', secondary=Book_Category, back_populates='categories')
