from re import match

from pymongo import MongoClient
from typing import Optional, List

from src.db.model import red_card, lineup
from src.db.model.goal import Goal
from src.db.model.match import Match
class MatchRepository:
    def __init__(self,client: MongoClient, db_name="eurozone", collection_name="match"):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]



    def search_match_by_id(self, match_id: int) -> dict | None:
        return self.collection.find_one({"id_match": match_id})

    def insert_goal_by_id(self, match_id: int, goal: Goal) -> bool:
        match = self.search_match_by_id(match_id)
        if not match:
            return False

        result = self.collection.update_one(
            {"id_match": match_id},
            {"$push": {"goals": goal.to_dict()}}
        )
        return result.modified_count > 0

    def insert_red_card(self,match_id:int, redc :red_card):
        match = self.search_match_by_id(match_id)
        if not match:
            return False
        print(match)
        result = self.collection.update_one(
            {"id_match": match_id},
            {"$push": {"red_cards":redc.to_dict()}}
        )
        print(result)
        return result.modified_count > 0
    def insert_home_linup(self, match_id:int, homel: List[lineup]):
        match = self.search_match_by_id(match_id)
        if not match:
            return False
        result = self.collection.update_one(
            {"id_match": match_id},
            {"$set": {"home_lineups": [p.to_dict() for p in homel]}}
        )
        return result.modified_count > 0

