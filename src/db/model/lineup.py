class Lineup:
    def __init__(self, id_player: int, start: str):
        self.id_player = id_player
        self.start = start

    def to_dict(self) -> dict:
        return {
            "id_player": self.id_player,
            "start": self.start
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_player=data["id_player"],
            start=data["start"]
        )
