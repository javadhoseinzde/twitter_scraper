import os

import pymongo
from dotenv import load_dotenv

load_dotenv()


class MongoConnection:
    def __init__(self, host=None, port=None, username=None, password=None):
        self.host = os.getenv("MONGODB_HOST", "localhost")
        self.port = int(os.getenv("MONGODB_PORT", 27017))
        self.username = os.getenv("MONGODB_USER")
        self.password = os.getenv("MONGODB_PASS")
        print(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/")
        self.client = pymongo.MongoClient(
            f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
        )
        self.client.close

    def connect(self):
        databases = self.client.list_database_names()
        print(databases)

    def insert_data(self, db, collection_name, data):
        try:
            db = self.client[db]
            collection = db[collection_name]
            collection.insert_one(data)
        except Exception as e:
            return e
