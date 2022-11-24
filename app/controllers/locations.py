from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.location import Location

from entity.sql.schemas import location_schema, locations_schema


def get_all():
    locations = Location.query.all()
    return locations_schema.dump(locations)


def get(id):
    location = Location.query.filter(Location.id == id).one_or_none()
    if location is not None:
        return location_schema.dump(location)
    else:
        abort(404, f"Location with id \"{id}\" not found.")


def create(location):
    new_location = location_schema.load(location, session=db.session)
    db.session.add(new_location)
    db.session.commit()
    return location_schema.dump(new_location), 201


def update(id, location):
    existing_location = Location.query.filter(Location.id == id).one_or_none()

    if existing_location:
        update_location = location_schema.load(location, session=db.session, instance=existing_location)
        db.session.merge(update_location)
        db.session.commit()
        return location_schema.dump(existing_location), 200
    else:
        abort(404, f"Location with id \"{id}\" not found.")


def delete(id):
    existing_location = Location.query.filter(Location.id == id).one_or_none()

    if existing_location:
        db.session.delete(existing_location)
        db.session.commit()
        return make_response(f"Location with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Location with id \"{id}\" not found.")
