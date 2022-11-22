from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.category import Category

from entity.sql.schemas import category_schema, categories_schema


def get_all():
    categories = Category.query.all()
    return categories_schema.dump(categories)


def get(id):
    category = Category.query.filter(Category.id == id).one_or_none()
    if category is not None:
        return category_schema.dump(category)
    else:
        abort(404, f"Category with id \"{id}\" not found.")


def create(category):
    new_category = category_schema.load(category, session=db.session)
    db.session.add(new_category)
    db.session.commit()
    return category_schema.dump(new_category), 201


def update(id, category):
    existing_category = Category.query.filter(Category.id == id).one_or_none()

    if existing_category:
        update_category = category_schema.load(category, session=db.session, instance=existing_category)
        db.session.merge(update_category)
        db.session.commit()
        return book_schema.dump(existing_category), 201
    else:
        abort(404, f"Category with id \"{id}\" not found.")


def delete(id):
    existing_category = Category.query.filter(Category.id == id).one_or_none()

    if existing_category:
        db.session.delete(existing_category)
        db.session.commit()
        return make_response(f"Category with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Category with id \"{id}\" not found.")
