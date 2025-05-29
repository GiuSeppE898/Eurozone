from pydantic import BaseModel

from src.db.model import Time


class Goal(BaseModel):
    international_name: str
    time : Time
    goal_type: str