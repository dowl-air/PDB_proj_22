
import os

MYSQL_DEFAULT_PORT = 3306

DB_USER = os.getenv('DB_USER', 'pdb')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pdb')
DB_HOST = os.getenv('DB_HOST', 'mysql')
DB_PORT = os.getenv('DB_PORT', MYSQL_DEFAULT_PORT)
DB_NAME = os.getenv('DB_NAME', 'pdb')

MONGO_DEFAULT_PORT = 27017

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'pdb')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'pdb')
MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME', 'mongodb')
MONGODB_PORT = os.getenv('MONGODB_PORT', MONGO_DEFAULT_PORT)
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'pdb')

KAFKA_DEFAULT_PORT = 9092

KAFKA_HOST = os.getenv('KAFKA_HOST', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', 29092)
