from dotenv import load_dotenv

import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus

load_dotenv()
DATABASE_USER = os.getenv("DBUSER")
DATABASE_PASSWORD = os.getenv("DBPASSWORD")
DATABASE_HOST = os.getenv("DBHOST")
DATABASE_COLLECTION_NAME = os.getenv("DBCOLLECTIONNAME")

uri = "mongodb://%s:%s@%s" % (
    quote_plus(DATABASE_USER),
    quote_plus(DATABASE_PASSWORD),
    DATABASE_HOST,
)


def getAll():
    try:
        client = MongoClient(uri)
        db = client.phaetons
        print(db.get_collection(DATABASE_COLLECTION_NAME).find_one({}))
        client.close()
    except ConnectionFailure:
        print("Server not available")


def insertJson(j):
    try:
        client = MongoClient(uri)
        db = client.phaetons
        collection = db[DATABASE_COLLECTION_NAME]
        collection.insert_many(j)
        client.close()
    except ConnectionFailure:
        print("Server not available")
