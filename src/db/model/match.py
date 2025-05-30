from datetime import datetime
from typing import Optional, List

from src.db.model.Stadio import Stadio
from src.db.model.goal import Goal
from src.db.model.lineup import Lineup
from src.db.model.events import Events


class Match:
    def __init__(
        self,
        id_match: int,
        home_team: str,
        away_team: str,
        home_score: float,
        away_score: float,
        home_penalty: Optional[int],
        away_penalty: Optional[int],
        home_score_total: float,
        away_score_total: float,
        winner: Optional[str],
        winner_reason: Optional[str],
        year: int,
        date: datetime,
        date_time: datetime,
        utc_offset_hours: float,
        group_name: Optional[str],
        matchday_name: str,
        status: str,
        type: str,
        round: str,
        round_mode: str,
        match_attendance: Optional[float],
        stadio: Stadio,
        goals: List[Goal],
        penalties_missed: float,
        penalties: float,
        red_cards: float,
        home_lineup: List[Lineup],
        away_lineup: List[Lineup],
        coach_home: str,
        coach_away: str,
        events: List[Events],
    ):
        self.id_match = id_match
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.home_penalty = home_penalty
        self.away_penalty = away_penalty
        self.home_score_total = home_score_total
        self.away_score_total = away_score_total
        self.winner = winner
        self.winner_reason = winner_reason
        self.year = year
        self.date = date
        self.date_time = date_time
        self.utc_offset_hours = utc_offset_hours
        self.group_name = group_name
        self.matchday_name = matchday_name
        self.status = status
        self.type = type
        self.round = round
        self.round_mode = round_mode
        self.match_attendance = match_attendance
        self.stadio = stadio
        self.goals = goals
        self.penalties_missed = penalties_missed
        self.penalties = penalties
        self.red_cards = red_cards
        self.home_lineup = home_lineup
        self.away_lineup = away_lineup
        self.coach_home = coach_home
        self.coach_away = coach_away
        self.events = events

    def to_dict(self) -> dict:
        return {
            "id_match": self.id_match,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "home_penalty": self.home_penalty,
            "away_penalty": self.away_penalty,
            "home_score_total": self.home_score_total,
            "away_score_total": self.away_score_total,
            "winner": self.winner,
            "winner_reason": self.winner_reason,
            "year": self.year,
            "date": self.date,
            "date_time": self.date_time,
            "utc_offset_hours": self.utc_offset_hours,
            "group_name": self.group_name,
            "matchday_name": self.matchday_name,
            "status": self.status,
            "type": self.type,
            "round": self.round,
            "round_mode": self.round_mode,
            "match_attendance": self.match_attendance,
            "stadio": self.stadio.to_dict() if self.stadio else None,
            "goals": [goal.to_dict() for goal in self.goals] if self.goals else [],
            "penalties_missed": self.penalties_missed,
            "penalties": self.penalties,
            "red_cards": self.red_cards,
            "home_lineups": [lineup.to_dict() for lineup in self.home_lineup] if self.home_lineup else [],
            "away_lineups": [lineup.to_dict() for lineup in self.away_lineup] if self.away_lineup else [],
            "coach_home": self.coach_home,
            "coach_away": self.coach_away,
            "events": [event.to_dict() for event in self.events] if self.events else [],
        }

    @classmethod
    def from_dict(cls, data: dict):
        def safe_list(data_field):
            return data_field if isinstance(data_field, list) else []

        return cls(
            id_match=data.get("id_match"),
            home_team=data.get("home_team", ""),
            away_team=data.get("away_team", ""),
            home_score=data.get("home_score", 0),
            away_score=data.get("away_score", 0),
            home_penalty=data.get("home_penalty"),
            away_penalty=data.get("away_penalty"),
            home_score_total=data.get("home_score_total", 0),
            away_score_total=data.get("away_score_total", 0),
            winner=data.get("winner"),
            winner_reason=data.get("winner_reason"),
            year=data.get("year", 0),
            date=data.get("date", datetime.utcnow()),
            date_time=data.get("date_time", datetime.utcnow()),
            utc_offset_hours=data.get("utc_offset_hours", 0.0),
            group_name=data.get("group_name"),
            matchday_name=data.get("matchday_name", ""),
            status=data.get("status", ""),
            type=data.get("type", ""),
            round=data.get("round", ""),
            round_mode=data.get("round_mode", ""),
            match_attendance=data.get("match_attendance"),
            stadio=Stadio.from_dict(data["stadio"]) if isinstance(data.get("stadio"), dict) else None,
            goals=[
                Goal.from_dict(g)
                for g in safe_list(data.get("goals"))
                if isinstance(g, dict)
            ],
            penalties_missed=data.get("penalties_missed", 0),
            penalties=data.get("penalties", 0),
            red_cards=data.get("red_cards", 0),
            home_lineup=[Lineup.from_dict(l) for l in data.get("home_lineups", [])],
            away_lineup=[Lineup.from_dict(l) for l in data.get("away_lineups", [])],
            coach_home=data.get("coach_home", "Unknown"),
            coach_away=data.get("coach_away", "Unknown"),
            events=[
                Events.from_dict(e)
                for e in safe_list(data.get("events"))
                if isinstance(e, dict)
            ],
        )