
from .Tempo import Tempo


class Red_Card:
    def __init__(self, time, international_name, country_code, phase, id_player):
        self.time = time
        self.international_name = international_name
        self.country_code = country_code
        self.phase = phase
        self.id_player = id_player

    def to_dict(self):
        return {
            "time": self.time.to_dict(),
            "international_name": self.international_name,
            "country_code": self.country_code,
            "phase": self.phase,
            "id_player": str(self.id_player)
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            phase = data.get("phase"),
            international_name = data.get("international_name"),
            country_code = data.get("country_code"),
            time=Tempo.from_dict(data["time"]) if data.get("time") else None,

        )
