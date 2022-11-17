
import sqlalchemy as sa

from .base import Base

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
