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

    def search_match_by_id(self, match_id: int) -> Match:
        match_data = self.collection.find_one({"id_match": match_id})
        if not match_data:
            return None
        return Match.from_dict(match_data)

    def add_goal(self, match: Match, home: bool):
        current_score = match.get(f"{'home' if home else 'away'}_score_total", 0)
        new_score = current_score + 1
        result = self.collection.update_one(
            {"id_match": match['id_match']},
            {"$set": {f"{'home' if home else 'away'}_score_total": new_score}}
        )
        
        return result.modified_count > 0
        

    def insert_goal(self, match_id: int, goal: Goal, assist_name: Optional[str] = None, assist_id: Optional[str] = None):
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
            "secondary_id_person": str(assist_id) if assist_id else None,
            "secondary_country_code": goal_dict.get("country_code") if assist_id is None else assist_id,
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


    def remove_event_from_match(self, match_id: int, event_id: str) -> bool:
        # Recupera il match
        match = self.search_match_by_id(match_id)
        if isinstance(match, Match):
            match = match.to_dict()

        if not match:
            print("[DEBUG] Match non trovato.")
            return False

        # Trova l'evento principale da rimuovere
        events = match.get("events", [])
        event_to_remove = next((e for e in events if e.get("id") == event_id), None)
        if not event_to_remove:
            print("[DEBUG] Evento con id specificato non trovato.")
            return False

        # Estrai i dati essenziali dell'evento
        target_phase = event_to_remove.get("phase")
        target_type = event_to_remove.get("type")
        target_name = event_to_remove.get("primary_name")
        target_minute = event_to_remove.get("time_minute")
        target_second = event_to_remove.get("time_second")

        # Prepara la query per rimuovere l'evento da events
        update_query = {
            "$pull": {
                "events": {"id": event_id}
            }
        }

        # Associa il tipo di evento all'array secondario corrispondente
        secondary_collections = {
            "GOAL": "goals",
            "RED_CARD": "red_cards",
            "PENALTY_SCORED": "penalties",
            "PENALTY_MISSED": "penalties_missed"
        }

        secondary_array_name = secondary_collections.get(target_type)

        # Se c'è un array secondario, cerca di rimuovere l'oggetto corrispondente
        if secondary_array_name and secondary_array_name in match:
            for item in match[secondary_array_name]:
                time = item.get("time", {})
                if (
                        #item.get("phase") == target_phase and
                        item.get("international_name") == target_name and
                        time.get("minute") == target_minute and
                        time.get("second") == target_second
                ):
                    update_query["$pull"][secondary_array_name] = item
                    break

        # Esegui l'update sul documento
        result = self.collection.update_one({"id_match": match_id}, update_query)

        # Debug info
        if result.modified_count == 0:
            print("[DEBUG] Nessuna modifica effettuata al documento.")
        else:
            print("[DEBUG] Evento rimosso con successo.")

        return result.modified_count > 0



    def insert_yellow_card(self, match_id: int, redc: red_card):
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
            "type": "YELLOW_CARD",
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
                    "events": red_card_event
                }
            }
        )

        return result.modified_count > 0

    def get_home_goal_count(self, match_id) -> int:
        match = self.search_match_by_id(match_id)
        return sum(
            1 for event in match['events']
            if (event['type'] == 'GOAL' or (event['type'] == 'PENALTY' and event['subType'] == 'SCORED'))
            and event['primary_country_code'] == match['home_team_code']
        )
        
    def get_away_goal_count(self, match_id) -> int:
        match = self.search_match_by_id(match_id)
        return sum(
            1 for event in match['events']
            if (event['type'] == 'GOAL' or (event['type'] == 'PENALTY' and event['subType'] == 'SCORED'))
            and event['primary_country_code'] == match['away_team_code']
        )


    #def count_matches_coached_by_name(self, coach_name: str) -> int:
    #    """
    #    Conta il numero di match in cui l'allenatore ha allenato come home o away coach.
    #    """
    #    return self.collection.count_documents({
    #        "$or": [
    #            {"home_coaches": coach_name},
    #            {"away_coaches": coach_name}
    #        ]
    #    })
