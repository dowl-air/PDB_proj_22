
import sqlalchemy as sa
from sqlalchemy.orm import relationship
import sqlalchemy.dialects.mysql as samysql

from .base import db

class BookCopy(db.Model):
	__tablename__ = 'book_copy'

	id = sa.Column(sa.Integer(), primary_key=True)
	book_id = sa.Column(sa.Integer(), sa.ForeignKey('book.id'), nullable=False)
	location_id = sa.Column(sa.Integer(), sa.ForeignKey('location.id'), nullable=False)
	print_date = sa.Column(sa.Date(), nullable=False)
	note = sa.Column(sa.VARCHAR(length=255))
	state = sa.Column(samysql.TINYINT(display_width=3), nullable=False, default=0)

	borrowals = relationship('Borrowal')
