import os

import pandas as pd
import pymongo
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")


class MongoDB:
    def __init__(self):
        # Create a new client and connect to the server
        self.client = pymongo.MongoClient(MONGO_URI, server_api=pymongo.server_api.ServerApi("1"))
        self.collection = self.connect_db("C4", "items")

    def connect_db(self, db_name, collection_name):
        # 만약 collection이 없다면 생성
        if collection_name not in self.client[db_name].list_collection_names():
            self.client[db_name].create_collection(collection_name)
        # collection 연결
        self.collection = self.client[db_name][collection_name]
        return self.collection

    def insert_one(self, data):
        self.collection.insert_one(data)

    def is_in(self, query):
        documents = self.collection.find(query)

        for doc in documents:
            return True

        return False
