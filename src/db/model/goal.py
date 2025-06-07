from .Tempo import Tempo


class Goal:
    def __init__(self, time, international_name, country_code, id_player):
        self.time = time
        self.international_name = international_name
        self.country_code = country_code
        self.id_player = id_player

    def to_dict(self):
        return {
            "time": self.time.to_dict(),
            "international_name": self.international_name,
            "country_code": self.country_code,
            "id_player": str(self.id_player)
        }

    @classmethod
    def from_dict(self, data: dict):
        return self(
            international_name=data["international_name"],
            time=Tempo.from_dict(data["time"]) if data.get("time") else None,
            goal_type=data["goal_type"]
        )