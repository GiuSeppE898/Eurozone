from re import match

from pymongo import MongoClient
from src.db.model.match import Match
class MatchRepository:
    def __init__(self,client: MongoClient, db_name="eurozone", collection_name="match"):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_match(self, match: Match):
        return self.collection.insert_one(match.to_dict())