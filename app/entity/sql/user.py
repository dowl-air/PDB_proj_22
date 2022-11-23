
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .. import UserRole
from .base import db


class User(db.Model):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer(), primary_key=True)
    first_name = sa.Column(sa.VARCHAR(length=255))
    last_name = sa.Column(sa.VARCHAR(length=255))
    role = sa.Column(sa.VARCHAR(length=255), nullable=False, default=UserRole.CUSTOMER)
    email = sa.Column(sa.VARCHAR(length=255), nullable=False, unique=True)
    password = sa.Column(sa.VARCHAR(length=255), nullable=False)

    reviews = relationship('Review')
    reservations = relationship('Reservation')
    borrowals = relationship('Borrowal')
