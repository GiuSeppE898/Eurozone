class Stadio:
    def __init__(
        self,
        stadium_id: int,
        stadium_name: str,
        stadium_city: str,
        stadium_country_code: str,
        stadium_capacity: int,
        stadium_latitude: complex,
        stadium_longitude: complex,
        stadium_pitch_length: float,
        stadium_pitch_width: float
    ):
        self.stadium_id = stadium_id
        self.stadium_name = stadium_name
        self.stadium_city = stadium_city
        self.stadium_country_code = stadium_country_code
        self.stadium_capacity = stadium_capacity
        self.stadium_latitude = stadium_latitude
        self.stadium_longitude = stadium_longitude
        self.stadium_pitch_length = stadium_pitch_length
        self.stadium_pitch_width = stadium_pitch_width

    def to_dict(self) -> dict:
        return {
            "stadium_id": self.stadium_id,
            "stadium_name": self.stadium_name,
            "stadium_city": self.stadium_city,
            "stadium_country_code": self.stadium_country_code,
            "stadium_capacity": self.stadium_capacity,
            "stadium_latitude": self.stadium_latitude,
            "stadium_longitude": self.stadium_longitude,
            "stadium_pitch_length": self.stadium_pitch_length,
            "stadium_pitch_width": self.stadium_pitch_width
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            stadium_id=data["stadium_id"],
            stadium_name=data["stadium_name"],
            stadium_city=data["stadium_city"],
            stadium_country_code=data["stadium_country_code"],
            stadium_capacity=data["stadium_capacity"],
            stadium_latitude=data["stadium_latitude"],
            stadium_longitude=data["stadium_longitude"],
            stadium_pitch_length=data["stadium_pitch_length"],
            stadium_pitch_width=data["stadium_pitch_width"]
        )