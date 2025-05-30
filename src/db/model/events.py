from datetime import datetime
from typing import Optional

class Events:
    def __init__(
        self,
        id: int,
        phase: str,
        timestamp: datetime,
        type: str,
        time_minute: float,
        time_second: float,
        primary_id_person: str,
        primary_country_code: str,
        primary_name: str,
        secondary_id_person: Optional[str] = None,
        secondary_country_code: Optional[str] = None,
        secondary_name: Optional[str] = None,
        body_part: Optional[str] = None,
        field_position_x: Optional[float] = None,
        field_position_y: Optional[float] = None,
        field_position_distance: Optional[float] = None
    ):
        self.id = id
        self.phase = phase
        self.timestamp = timestamp
        self.type = type
        self.time_minute = time_minute
        self.time_second = time_second
        self.primary_id_person = primary_id_person
        self.primary_country_code = primary_country_code
        self.primary_name = primary_name
        self.secondary_id_person = secondary_id_person
        self.secondary_country_code = secondary_country_code
        self.secondary_name = secondary_name
        self.body_part = body_part
        self.field_position_x = field_position_x
        self.field_position_y = field_position_y
        self.field_position_distance = field_position_distance

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phase": self.phase,
            "timestamp": self.timestamp,
            "type": self.type,
            "time_minute": self.time_minute,
            "time_second": self.time_second,
            "primary_id_person": self.primary_id_person,
            "primary_country_code": self.primary_country_code,
            "primary_name": self.primary_name,
            "secondary_id_person": self.secondary_id_person,
            "secondary_country_code": self.secondary_country_code,
            "secondary_name": self.secondary_name,
            "body_part": self.body_part,
            "field_position_x": self.field_position_x,
            "field_position_y": self.field_position_y,
            "field_position_distance": self.field_position_distance
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            phase=data["phase"],
            timestamp=data["timestamp"],
            type=data["type"],
            time_minute=data["time_minute"],
            time_second=data["time_second"],
            primary_id_person=data["primary_id_person"],
            primary_country_code=data["primary_country_code"],
            primary_name=data["primary_name"],
            secondary_id_person=data.get("secondary_id_person"),
            secondary_country_code=data.get("secondary_country_code"),
            secondary_name=data.get("secondary_name"),
            body_part=data.get("body_part"),
            field_position_x=data.get("field_position_x"),
            field_position_y=data.get("field_position_y"),
            field_position_distance=data.get("field_position_distance")
        )