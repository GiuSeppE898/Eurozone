class Stadio:
    def __init__(
        self,
        id: int,
        name: str,
        name_official: str,
        city: str,
        country_code: str,
        capacity: float,
        latitude: float,
        longitude: float,
        pitch_length: float,
        pitch_width: float,
    ):
        self.id = id
        self.name = name
        self.name_official = name_official
        self.city = city
        self.country_code = country_code
        self.capacity = capacity
        self.latitude = latitude
        self.longitude = longitude
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_official": self.name_official,
            "city": self.city,
            "country_code": self.country_code,
            "capacity": self.capacity,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "pitch_length": self.pitch_length,
            "pitch_width": self.pitch_width,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            name_official=data.get("name_official", ""),
            city=data.get("city", ""),
            country_code=data.get("country_code", ""),
            capacity=data.get("capacity", 0.0),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            pitch_length=data.get("pitch_length", 0.0),
            pitch_width=data.get("pitch_width", 0.0),
        )