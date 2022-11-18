
import sqlalchemy as sa

from .base import db

Book_Author = db.Table(
	'Book_Author',
	sa.Column('Bookid', sa.Integer(), sa.ForeignKey('book.id'), primary_key=True),
	sa.Column('Authorid', sa.Integer(), sa.ForeignKey('author.id'), primary_key=True)
)

Book_Category = db.Table(
	'Book_Category',
	sa.Column('Bookid', sa.Integer(), sa.ForeignKey('book.id'), primary_key=True),
	sa.Column('Categoryid', sa.Integer(), sa.ForeignKey('category.id'), primary_key=True)
)
