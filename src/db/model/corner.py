from cmath import phase
from .Tempo import Tempo

class Corner:
    def __init__(self, id_player: str, country_code: str, international_name: str, time: dict, phase: str):
        self.id_player = id_player
        self.country_code = country_code
        self.international_name = international_name
        self.time = time  # es: {"minute": 35, "second": 12}
        self.phase = phase

    def to_dict(self):
        return {
            "id_player": str(self.id_player),
            "country_code": self.country_code,
            "international_name": self.international_name,
            "time": self.time,
            "phase": self.phase
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            phase = data.get("phase"),
            international_name = data.get("international_name"),
            country_code = data.get("country_code"),
            time = Tempo.from_dict(data["time"]) if data.get("time") else None,
            id_player = data.get("id_player", None)
        )
