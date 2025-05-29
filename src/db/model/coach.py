class Coach:
    def __init__(self, name, country, country_code, role, id_match, year):
        self.name = name
        self.country = country
        self.country_code = country_code
        self.role = role
        self.id_match = id_match
        self.year = year

    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "country_code": self.country_code,
            "role": self.role,
            "id_match": self.id_match,
            "year": self.year
        }

    @staticmethod
    def from_dict(data: dict) -> "Coach":
        return Coach(
            name=data.get("name"),
            country=data.get("country"),
            country_code=data.get("country_code"),
            role=data.get("role"),
            id_match=data.get("id_match"),
            year=data.get("year")
        )
