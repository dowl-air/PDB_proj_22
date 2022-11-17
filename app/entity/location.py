
import sqlalchemy as sa

from .base import Base

class Location(Base):
	__tablename__ = 'location'

	id = sa.Column(sa.Integer(), primary_key=True)
	name = sa.Column(sa.VARCHAR(length=255), nullable=False)
	address = sa.Column(sa.VARCHAR(length=255))
