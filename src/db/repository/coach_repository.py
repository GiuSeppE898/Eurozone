from pymongo import MongoClient
from db.model.coach import Coach

class CoachRepository:
    def __init__(self, client: MongoClient, db_name="eurozone", collection_name="coaches"):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_coach(self, coach: Coach):
        return self.collection.insert_one(coach.to_dict())

    def find_coach_by_name_and_year(self, name: str, year: int):
        data = self.collection.find_one({'name': name, 'year': year})
        return Coach.from_dict(data) if data else None

    def update_coach(self, coach: Coach):
        return self.collection.update_one(
            {"name": coach.name, "year": coach.year},
            {"$set": coach.to_dict()}
        )

    def delete_coach_by_name_and_year(self, name: str, year: int):
        return self.collection.delete_one({"name": name, "year": year})


    def get_coach_stats(self, coach_name: str) -> tuple[int, list[int]]:
        query = {
            "$or": [
                {"home_coaches.name": coach_name},
                {"away_coaches.name": coach_name}
            ]
        }

        matches = list(self.collection.find(query, {"id_match": 1, "year": 1}))

        unique_match_ids = set()
        years = set()

        for match in matches:
            unique_match_ids.add(match["id_match"])
            years.add(match["year"])

        return len(unique_match_ids), sorted(years)