from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.location import Location
from entity.sql.schemas import location_schema, locations_schema

from entity.nosql.location import Location as MongoLocation
from entity.nosql.schemas_mongo import location_schema as mongo_location_schema
from entity.nosql.schemas_mongo import locations_schema as mongo_locations_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_all():
    # Get all locations from mongo database
    locations = MongoLocation.objects
    return mongo_locations_schema.dump(locations)


def get(id):
    # Get one location from mongo database
    try:
        location = MongoLocation.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Location with id {id} not found.")

    return mongo_location_schema.dump(location)


def create(location):
    new_location = location_schema.load(location, session=db.session)
    db.session.add(new_location)
    db.session.commit()

    producer.send(KafkaTopic.LOCATION.value, key=KafkaKey.CREATE.value, value=location_schema.dump(new_location))

    return location_schema.dump(new_location), 201


def update(id, location):
    existing_location = Location.query.filter(Location.id == id).one_or_none()

    if not existing_location:
        abort(404, f"Location with id {id} not found.")

    update_location = location_schema.load(location, session=db.session, instance=existing_location)
    db.session.merge(update_location)
    db.session.commit()

    producer.send(KafkaTopic.LOCATION.value, key=KafkaKey.UPDATE.value, value=location_schema.dump(update_location))

    return location_schema.dump(update_location), 200


def delete(id):
    existing_location = Location.query.filter(Location.id == id).one_or_none()

    if not existing_location:
        abort(404, f"Location with id {id} not found.")

    db.session.delete(existing_location)
    db.session.commit()

    producer.send(KafkaTopic.LOCATION.value, key=KafkaKey.DELETE.value, value={"id": int(id)})

    return make_response(f"Location with id {id} successfully deleted.", 200)
