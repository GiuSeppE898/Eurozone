from .Tempo import Tempo


class Goal:
    def __init__(self, time, international_name, goal_type = None, country_code=None, id_player=None):
        self.time = time
        self.international_name = international_name
        self.goal_type = goal_type
        self.country_code = country_code
        self.id_player = id_player

    def to_dict(self):
        return {
            "time": self.time.to_dict(),
            "international_name": self.international_name,
            "goal_type": self.goal_type,
            "country_code": self.country_code,
            "id_player": self.id_player
        }

    @classmethod
    def from_dict(self, data: dict):
        return self(
            time=Tempo.from_dict(data["time"]) if data.get("time") else None,
            international_name=data["international_name"],
            goal_type=data["goal_type"] if "goal_type" in data else None,
            country_code=data.get("country_code") if "country_code" in data else None,
            id_player=data.get("id_player") if "id_player" in data else None
        )