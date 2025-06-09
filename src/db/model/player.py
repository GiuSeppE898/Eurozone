from bson import ObjectId

class Player:
    def __init__(self, name: str, name_shirt: str, jersey_number: float, position_national: str, 
                 position_field: str, birth_date: str, id_match: int, id_player: int, 
                 start: str, year: int, id_club: int, country_code: int):
        self.id_player = id_player
        self.name = name
        self.country_code = country_code
        self.birth_date = birth_date
        self.name_shirt = name_shirt
        self.jersey_number = jersey_number
        self.position_national = position_national
        self.position_field = position_field
        self.id_match = id_match
        self.start = start
        self.year = year
        self.id_club = id_club

    def to_dict(self) -> dict:
        return {
            "id_player": self.id_player,
            "name": self.name,
            "country_code": self.country_code,
            "birth_date": self.birth_date,
            "name_shirt": self.name_shirt,
            "jersey_namber": self.jersey_number,
            "position_national": self.position_national,
            "position_field": self.position_field,
            "id_match": self.id_match,
            "start": self.start,
            "year": self.year,
            "id_club": self.id_club,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_player=data["id_player"],
            name=data["name"],
            country_code=data["country_code"],
            birth_date=data["birth_date"],
            name_shirt=data["name_shirt"],
            jersey_number=data["jersey_namber"],
            position_national=data["position_national"],
            position_field=data["position_field"],
            id_match=data["id_match"],
            start=data["start"],
            year=data["year"],
            id_club=data["id_club"],
        )
