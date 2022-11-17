
import sqlalchemy as sa

from .base import Base

class Review(Base):
	__tablename__ = 'review'

	id = sa.Column(sa.Integer(), primary_key=True)
	user_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), nullable=False)
	book_id = sa.Column(sa.Integer(), sa.ForeignKey('book.id'), nullable=False)
	title = sa.Column(sa.VARCHAR(length=255), nullable=False)
	content = sa.Column(sa.VARCHAR(length=1000))
	rating = sa.Column(sa.Integer(), nullable=False)
