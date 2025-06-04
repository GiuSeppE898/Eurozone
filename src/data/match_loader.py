import ast
import pandas as pd
import json

class MatchLoader:
    def __init__(self, path: str):
        self.path = path
    
    def parse_field(self, value):
        if isinstance(value, str):
            processed_value = value.replace('nan', 'None')
            try:
                return ast.literal_eval(processed_value)
            except (ValueError, SyntaxError):
                return value
        return value

    def filter_lineups(self, lineups_data):
        """
        Filtra una lista di dizionari di giocatori, mantenendo solo alcune chiavi.
        """
        if not isinstance(lineups_data, list):
            return lineups_data

        filtered_players = []
        for player in lineups_data:
            if isinstance(player, dict):
                # nuovo dizionario con solo le chiavi desiderate
                filtered_player = {
                    #"name": player.get("name"),
                    #"position_national": player.get("position_national"),
                    "id_player": player.get("id_player"),
                    #"country_code": player.get("country_code"),
                    "start": player.get("start")
                }
                filtered_players.append(filtered_player)
            else:
                filtered_players.append(player)
        return filtered_players

    def filter_coach_name(self, coaches_data):
        if isinstance(coaches_data, list) and coaches_data:
            first_coach = coaches_data[0]
            if isinstance(first_coach, dict):
                return first_coach.get("name")
        return None

    def filter_goals(self, goals_data):
        """
        Filtra una lista di dizionari di goal, mantenendo solo le chiavi specificate.
        """
        if not isinstance(goals_data, list):
            # Se i dati non sono una lista, restituisce come sono.
            return goals_data

        filtered_goals = []
        for goal in goals_data:
            if isinstance(goal, dict):
                # Crea un nuovo dizionario con solo le chiavi desiderate
                filtered_goal = {
                    "international_name": goal.get("international_name"),
                    "time": goal.get("time"),
                    "goal_type": goal.get("goal_type")
                }
                filtered_goals.append(filtered_goal)
            else:
                filtered_goals.append(goal)
        return filtered_goals

    def filter_penalties(self, pen_data):
        if not isinstance(pen_data, list):
            return pen_data  # o [], a seconda di cosa ti serve

        filtered_penalties = []
        for p in pen_data:
            if isinstance(p, dict):
                filtered_penalty = {
                    "phase": p.get("phase"),
                    "time": p.get("time"),
                    "international_name": p.get("international_name"),
                    "penalty_type": p.get("penalty_type"),
                    "country_code": p.get("country_code")
                }
                filtered_penalties.append(filtered_penalty)
        return filtered_penalties

    def filter_cards(self, cards_data):
        if not isinstance(cards_data, list):
            return cards_data
        filtered_cards = []
        for p in cards_data:
            if isinstance(p, dict):
                filtered_card = {
                    "phase": p.get("phase"),
                    "time": p.get("time"),
                    "international_name": p.get("international_name"),
                    "country_code": p.get("country_code")
                }
                filtered_cards.append(filtered_card)
        return filtered_cards

    def load(self, debug=False):
        all_documents = []
        for x in range(1960, 2025, 4):
            try:
                if debug:
                    print(f"Caricamento: {self.path}/{x}.csv")
                df = pd.read_csv(f"{self.path}/{x}.csv")
                for _, row in df.iterrows():
                    doc = {}
                    stadium_fields = {}
                    for col in df.columns:
                        columns_to_exclude = [
                            "game_referees",
                            "condition_humidity",
                            "condition_pitch",
                            "condition_temperature",
                            "condition_weather",
                            "condition_wind_speed",
                            "stadium_name_sponsor",
                            "stadium_name_media",
                            "stadium_name_event"
                        ]
                        if col in columns_to_exclude:
                            continue

                        parsed_value = self.parse_field(row[col])
                        if col.startswith("stadium_"):
                            stadium_key = col.replace("stadium_", "")
                            stadium_fields[stadium_key] = parsed_value
                            continue
                        if col == "goals":
                            doc[col] = self.filter_goals(parsed_value)
                        elif col == "home_lineups" or col == "away_lineups":
                            doc[col] = self.filter_lineups(parsed_value)
                        elif col in ["home_coaches", "away_coaches"]:
                            doc[col] = self.filter_coach_name(parsed_value)
                        elif col == "penalties":
                            doc["penalties"] = self.filter_penalties(parsed_value)
                        elif col == "penalties_missed":
                            doc["penalties_missed"] = self.filter_penalties(parsed_value)
                        elif col == "red_cards":
                            doc["red_cards"] = self.filter_cards(parsed_value)

                        else:
                            doc[col] = parsed_value
                    if stadium_fields:
                        doc["stadio"] = stadium_fields

                    if "id_match" in doc:
                        try:
                            doc["_id"] = int(doc["id_match"])
                        except (ValueError, TypeError):
                            doc["_id"] = doc["id_match"]

                    all_documents.append(doc)

            except FileNotFoundError:
                if debug:
                    print(f"File euro/{x}.csv non trovato. Saltando.")
            except Exception as e:
                print(f"Errore durante l'elaborazione dell'anno {x}: {e}")
        return all_documents




