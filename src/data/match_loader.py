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
                    "name": player.get("name"),
                    "position_national": player.get("position_national"),
                    "id_player": player.get("id_player"),
                    "country_code": player.get("country_code"),
                    "start": player.get("start")
                }
                filtered_players.append(filtered_player)
            else:
                filtered_players.append(player)
        return filtered_players


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
                # Se un elemento nella lista non è un dizionario, lo include così com'è
                filtered_goals.append(goal)
        return filtered_goals

    def load_and_save(self, output_path: str):
        for x in range(1960, 2025, 4):
            try:
                df = pd.read_csv(f"{self.path}/{x}.csv")
                documents = []
                for _, row in df.iterrows():
                    doc = {}
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
                            "stadium_name_official",
                            "stadium_name_event"
                        ]
                        if col in columns_to_exclude:
                            continue
                        parsed_value = self.parse_field(row[col])
                        if col == "goals":
                            doc[col] = self.filter_goals(parsed_value)
                        elif col == "home_lineups" or col == "away_lineups":
                            doc[col] = self.filter_lineups(parsed_value)


                        else:
                            doc[col] = parsed_value

                    if "id_match" in doc:
                        try:
                            doc["_id"] = int(doc["id_match"])
                        except (ValueError, TypeError):
                            print(f"Attenzione: 'id_match' non è un numero valido per il documento nell'anno {x}.")
                            doc["_id"] = doc["id_match"] # Mantiene il valore originale se non è convertibile

                    documents.append(doc)


                with open(f"{output_path}/{x}.json", "w", encoding="utf-8") as f:
                    json.dump(documents, f, ensure_ascii=False, indent=2)

                print(f"Conversione completata. File salvato come {output_path}/{x}.json.")

            except FileNotFoundError:
                print(f"Errore: Il file euro/{x}.csv non è stato trovato. Saltando l'anno {x}.")
            except Exception as e:
                print(f"Si è verificato un errore durante l'elaborazione dell'anno {x}: {e}")

