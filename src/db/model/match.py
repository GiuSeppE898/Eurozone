from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from src.db.model import goal
from src.db.model.Stadio import Stadio
from src.db.model.lineup import lineup

from src.db.model.events import events




class match(BaseModel):
    id_match : int
    home_team : str
    away_team : str
    home_score: float
    away_score : float
    home_penalty: Optional[int] = None
    away_penalty: Optional[int] = None
    home_score_total : float
    away_score_total : float
    winner : Optional[str] = None
    winner_reason: Optional[str] = None
    year : int
    date: datetime
    date_time: datetime
    utc_offset_hours: float
    group_name: Optional[str] = None
    matchday_name: str
    status: str
    type: str
    round: str
    round_mode: str
    match_attendance: Optional[float] = None
    stadio : Stadio
    goals: List[goal]
    penalties_missed: float
    penalties : float
    red_cards : float
    home_lineup : List[lineup]
    away_lineup: List[lineup]
    coach_home: str
    coach_away: str
    events : List[events]

