import uuid

from pymongo import MongoClient
from typing import Optional, List

from ..model import red_card, lineup
from ..model.goal import Goal
from ..model.match import Match
class MatchRepository:
    def __init__(self,client: MongoClient, db_name="eurozone", collection_name="match"):
        self.client = client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_match(self, match: Match):
        return self.collection.insert_one(match.to_dict())

    def search_match_by_id(self, match_id: int) -> dict | None:
        print(match_id)
        return self.collection.find_one({"id_match": match_id})


    def insert_goal(self, match_id: int, goal: Goal, assist_name: Optional[str] = None):
        match = self.search_match_by_id(match_id)
        if not match:
            return False

        goal_dict = goal.to_dict()
        event_id = str(uuid.uuid4())
        minute = goal_dict["time"]["minute"]
        phase = "FIRST_HALF" if minute <= 45 else "SECOND_HALF"

        event_goal = {
            "id": event_id,
            "phase": phase,
            "timestamp": None,
            "type": "GOAL",
            "subType": None,
            "time_minute": minute,
            "time_second": goal_dict["time"]["second"],
            "primary_id_person": goal_dict.get("id_player"),
            "primary_country_code": goal_dict.get("country_code"),
            "primary_name": goal_dict.get("international_name"),
            "secondary_id_person": None,
            "secondary_country_code": None,
            "secondary_name": assist_name if assist_name else None,
            "body_part": None,
            "field_position_x": None,
            "field_position_y": None,
            "field_position_distance": None,
            "field_position_zone": None
        }

        result = self.collection.update_one(
            {"id_match": match_id},
            {
                "$push": {
                    "goals": goal_dict,
                    "events": event_goal
                }
            }
        )
        return result.modified_count > 0


    def insert_red_card(self, match_id: int, redc: red_card):
        match = self.search_match_by_id(match_id)
        if not match:
            return False

        red_card_data = redc.to_dict()
        minute = red_card_data["time"]["minute"]
        second = red_card_data["time"].get("second")
        red_card_event = {
            "id": str(uuid.uuid4()),
            "phase": red_card_data["phase"],
            "timestamp": None,
            "type": "RED_CARD",
            "subType": None,
            "time_minute": minute,
            "time_second": second,
            "primary_id_person": red_card_data.get("id_player"),
            "primary_country_code": red_card_data.get("country_code"),
            "primary_name": red_card_data.get("international_name"),
            "secondary_id_person": red_card_data.get("id_player"),
            "secondary_country_code": red_card_data.get("country_code"),
            "secondary_name": red_card_data.get("international_name"),
            "body_part": None,
            "field_position_x": None,
            "field_position_y": None,
            "field_position_distance": None,
            "field_position_zone": None
        }

        result = self.collection.update_one(
            {"id_match": match_id},
            {
                "$push": {
                    "red_cards": red_card_data,
                    "events": red_card_event
                }
            }
        )

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

    def insert_away_linup(self, match_id:int, homel: List[lineup]):
        match = self.search_match_by_id(match_id)
        if not match:
            return False
        result = self.collection.update_one(
            {"id_match": match_id},
            {"$set": {"away_lineups": [p.to_dict() for p in homel]}}
        )
        return result.modified_count > 0



    def count_goals_by_player_name(self, player_name: str) -> int:
        """
        Conta il numero totale di goal segnati da un giocatore dato il suo nome.
        """
        pipeline = [
            {"$unwind": "$goals"},
            {"$match": {"goals.international_name": player_name}},
            {"$count": "total_goals"}
        ]

        result = list(self.collection.aggregate(pipeline))
        return result[0]["total_goals"] if result else 0

    def get_match_from_edition(self,edition:int) -> list[dict]:
        return list(self.collection.find({"year": edition}))



    # script per trovare il totale dei match giocati

    def count_matches_played_by_player_id(self, player_id: int) -> int:
        player_id_str = str(player_id)
        return self.collection.count_documents({
            "$or": [
                {"home_lineups.id_player": player_id_str},
                {"away_lineups.id_player": player_id_str}
            ]
        })

    #script per trovare il totale dei match giocati da titolare

    def count_matches_started_by_player_id(self, player_id: int) -> int:
        player_id_str = str(player_id)
        return self.collection.count_documents({
            "$or": [
                {"home_lineups": {"$elemMatch": {"id_player": player_id_str, "start": "field"}}},
                {"away_lineups": {"$elemMatch": {"id_player": player_id_str, "start": "field"}}}
            ]
        })

    #script per contare gli assist
    def count_assists_by_player_id(self, player_id: int) -> int:
        player_id_str = str(player_id)

        matches_with_assists = self.collection.find({
            "events": {
                "$elemMatch": {
                    "type": "GOAL",
                    "secondary_id_person": player_id_str
                }
            }
        })

        assist_count = 0
        for match in matches_with_assists:
            for event in match.get("events", []):
                if (
                        event.get("type") == "GOAL"
                        and event.get("secondary_id_person") == player_id_str
                ):
                    assist_count += 1

        return assist_count