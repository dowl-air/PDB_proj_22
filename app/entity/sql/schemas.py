from marshmallow_sqlalchemy import fields

from .base import ma
from . import *


class BorrowalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Borrowal
        load_instance = True
        sqla_session = db.session


borrowal_schema = BorrowalSchema()
borrowals_schema = BorrowalSchema(many=True)


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        sqla_session = db.session


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


class ReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation
        load_instance = True
        sqla_session = db.session


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
        sqla_session = db.session
    # books


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        sqla_session = db.session
    # books


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class BookCopySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookCopy
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    borrowals = fields.Nested(BorrowalSchema, many=True)


book_copy_schema = BookCopySchema()
book_copies_schema = BookCopySchema(many=True)


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    copies = fields.Nested(BookCopySchema, many=True)
    reviews = fields.Nested(ReviewSchema, many=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    reviews = fields.Nested(ReviewSchema, many=True)
    borrowals = fields.Nested(BorrowalSchema, many=True)
    reservations = fields.Nested(ReservationSchema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
