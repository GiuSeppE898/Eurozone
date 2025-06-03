
from src.db.model.Tempo import Tempo


class Red_Card:
    def __init__(self,
                 phase:str,
                 international_name:str,
                 country_code:str,
                 time: Tempo,
                 ):
        self.time = time
        self.phase = phase
        self.international_name = international_name
        self.country_code = country_code


    def to_dict(self):
        return{
            "phase":self.phase,
            "international_name":self.international_name,
            "country_code" :self.country_code,
            "time": self.time.to_dict() if self.time else None,
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            phase = data.get("phase"),
            international_name = data.get("international_name"),
            country_code = data.get("country_code"),
            time=Tempo.from_dict(data["time"]) if data.get("time") else None,

        )
