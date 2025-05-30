from datetime import datetime
from typing import Optional

class Events:
    def __init__(
        self,
        id: str,
        phase: Optional[str],
        timestamp: Optional[datetime],
        type: Optional[str],
        subType: Optional[str] = None,
        time_minute: Optional[float] = None,
        time_second: Optional[float] = None,
        primary_id_person: Optional[str] = None,
        primary_country_code: Optional[str] = None,
        primary_name: Optional[str] = None,
        secondary_id_person: Optional[str] = None,
        secondary_country_code: Optional[str] = None,
        secondary_name: Optional[str] = None,
        body_part: Optional[str] = None,
        field_position_x: Optional[float] = None,
        field_position_y: Optional[float] = None,
        field_position_distance: Optional[float] = None,
        field_position_zone: Optional[str] = None
    ):
        self.id = id
        self.phase = phase
        self.timestamp = timestamp
        self.type = type
        self.subType = subType
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
        self.field_position_zone = field_position_zone

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phase": self.phase,
            "timestamp": self.timestamp,
            "type": self.type,
            "subType": self.subType,
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
            "field_position_distance": self.field_position_distance,
            "field_position_zone": self.field_position_zone
        }

    @classmethod
    def from_dict(cls, data: dict):
        from dateutil.parser import isoparse

        # Convert timestamp string to datetime or None
        ts = data.get("timestamp")
        if isinstance(ts, str):
            try:
                ts = isoparse(ts)
            except Exception:
                ts = None

        return cls(
            id=data.get("id"),
            phase=data.get("phase"),
            timestamp=ts,
            type=data.get("type"),
            subType=data.get("subType"),
            time_minute=data.get("time_minute"),
            time_second=data.get("time_second"),
            primary_id_person=data.get("primary_id_person"),
            primary_country_code=data.get("primary_country_code"),
            primary_name=data.get("primary_name"),
            secondary_id_person=data.get("secondaty_id_person") or data.get("secondary_id_person"),
            secondary_country_code=data.get("secondaty_country_code") or data.get("secondary_country_code"),
            secondary_name=data.get("secondaty_name") or data.get("secondary_name"),
            body_part=data.get("body_part"),
            field_position_x=data.get("field_position_x"),
            field_position_y=data.get("field_position_y"),
            field_position_distance=data.get("field_position_distance"),
            field_position_zone=data.get("field_position_zone")
        )