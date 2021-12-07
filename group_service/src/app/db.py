from pymongo import MongoClient
from .config import get_database_uri

MONGO_DATABASE_URI = get_database_uri()

client = MongoClient(MONGO_DATABASE_URI)

db = client['groups']

group_collection = db['groups']

