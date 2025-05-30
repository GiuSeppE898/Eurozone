from src.db.model.Tempo import Tempo

class Goal:
    def __init__(self, international_name: str, time: Tempo, goal_type: str):
        self.international_name = international_name
        self.time = time
        self.goal_type = goal_type

    def to_dict(self) -> dict:
        return {
            "international_name": self.international_name,
            "time": self.time.to_dict() if self.time else None,
            "goal_type": self.goal_type
        }

    @classmethod
    def from_dict(self, data: dict):
        return self(
            international_name=data["international_name"],
            time=Tempo.from_dict(data["time"]) if data.get("time") else None,
            goal_type=data["goal_type"]
        )