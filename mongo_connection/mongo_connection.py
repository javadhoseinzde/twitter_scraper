import pymongo



class MongoConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port

        self.username = username
        self.password = password
        self.client = pymongo.MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/")

    def connect(self):
        databases = self.client.list_database_names()
        print(databases)

    def create_collection(self, collection_name):
        if collection_name in self.client.list_database_names():
            return "collection already exists"
        else:
            db = self.client[collection_name]

            collection = db[collection_name]

            collection.insert_one({"name": "example", "value": 123})

            dblist = self.client.list_database_names()
            print("Databases after insert:", dblist)

    def insert_data(self, collection_name, data):
        try:
            db = self.client[collection_name]
            collection = db[collection_name]
            collection.insert_one(data)
        except Exception as e:
            return e