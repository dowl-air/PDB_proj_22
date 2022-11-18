
import sqlalchemy as sa
import sqlalchemy.dialects.mysql as samysql

from .base import db

class Reservation(db.Model):
	__tablename__ = 'reservation'

	id = sa.Column(sa.Integer(), primary_key=True)
	book_copy_id = sa.Column(sa.Integer(), sa.ForeignKey('book_copy.id'), nullable=False)
	customer_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), nullable=False)
	start_date = sa.Column(sa.Date(), nullable=False)
	end_date = sa.Column(sa.Date(), nullable=False)
	state = sa.Column(samysql.TINYINT(display_width=3), nullable=False, default=0)
