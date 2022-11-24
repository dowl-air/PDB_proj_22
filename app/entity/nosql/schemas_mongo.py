import marshmallow_mongoengine as ma

from . import *


class BorrowalSchema(ma.ModelSchema):
    class Meta:
        model = Borrowal


borrowal_schema = BorrowalSchema()
borrowals_schema = BorrowalSchema(many=True)


class ReviewSchema(ma.ModelSchema):
    class Meta:
        model = Review


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


class ReservationSchema(ma.ModelSchema):
    class Meta:
        model = Reservation


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class BookCopySchema(ma.ModelSchema):
    class Meta:
        model = BookCopy


book_copy_schema = BookCopySchema()
book_copies_schema = BookCopySchema(many=True)


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
