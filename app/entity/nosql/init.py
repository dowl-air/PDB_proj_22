
import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import mongoengine as me

MONGO_DEFAULT_PORT = 27017

def mongo_connect(host: str = 'localhost', port: int = MONGO_DEFAULT_PORT, timeout: int = 3000) -> MongoClient:
	conn: MongoClient = me.connect('pdb', serverSelectionTimeoutMS=timeout)

	try:
		conn.admin.command('ping')
	except ConnectionFailure:
		print('Failed to connect to the database server at %s:%i' % (host, port), file=sys.stderr)
		sys.exit(1)

	return conn
