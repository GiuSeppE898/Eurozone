from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.db.model import goal


class events(BaseModel):
    id: int
    phase: str
    timestamp: datetime
    type: str
    time_minute: float
    time_second: float
    primary_id_person: str
    primary_country_code: str
    primary_name: str
    secondaty_id_person: Optional[str] = None
    secondaty_country_code: Optional[str] = None
    secondaty_name: Optional[str] = None
    body_part: Optional[str] = None
    field_position_x: Optional[float] = None
    field_position_y: Optional[float] = None
    field_position_distance: Optional[float] = None

