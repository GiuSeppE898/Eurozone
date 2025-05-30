class Tempo:
    def __init__(self, minute: int, second: int):
        self.minute = minute
        self.second = second

    def to_dict(self) -> dict:
        return {
            "minute": self.minute,
            "second": self.second
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            minute=data["minute"],
            second=data.get("second", 0)
        )