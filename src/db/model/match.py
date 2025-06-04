from datetime import datetime
from typing import Optional, List

from db.model.Stadio import Stadio
from db.model.goal import Goal
from db.model.lineup import Lineup
from db.model.events import Events
from db.model.penalty import Penalty
from db.model.red_card import Red_Card


class Match:
    def __init__(
        self,
        id_match: int,
        home_team: str,
        away_team: str,
        home_team_code: str,
        away_team_code: str,
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
        penalties_missed: List[Penalty],
        penalties: List[Penalty],
        red_cards: List[Red_Card],
        home_lineup: List[Lineup],
        away_lineup: List[Lineup],
        home_coaches: str,
        away_coaches: str,
        events: List[Events],
    ):
        self.id_match = id_match
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_code = home_team_code
        self.away_team_code = away_team_code
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
        self.home_coaches = home_coaches
        self.away_coaches = away_coaches
        self.events = events

    def to_dict(self) -> dict:
        return {
            "id_match": self.id_match,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_team_code": self.home_team_code,
            "away_team_code": self.away_team_code,
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
            "penalties_missed": [penalty.to_dict() for penalty in self.penalties_missed] if self.penalties_missed else [],
            "penalties": [penalty.to_dict() for penalty in self.penalties] if self.penalties else [],
            "red_cards": [red_card.to_dict() for red_card in self.red_cards] if self.red_cards else [],
            "home_lineups": [lineup.to_dict() for lineup in self.home_lineup] if self.home_lineup else [],
            "away_lineups": [lineup.to_dict() for lineup in self.away_lineup] if self.away_lineup else [],
            "home_coaches": self.home_coaches,
            "away_coaches": self.away_coaches,
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
            home_team_code=data.get("home_team_code", ""),
            away_team_code=data.get("away_team_code", ""),
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
            penalties_missed=[
                Penalty.from_dict(p)
                for p in safe_list(data.get("penalties_missed"))
                if isinstance(p, dict)
            ],
            penalties=[
                Penalty.from_dict(p)
                for p in safe_list(data.get("penalties"))
                if isinstance(p, dict)
            ],
            red_cards=[
                Red_Card.from_dict(r)
                for r in safe_list(data.get("red_cards"))
                if isinstance(r, dict)
            ],
            home_lineup=[Lineup.from_dict(l) for l in data.get("home_lineups", [])],
            away_lineup=[Lineup.from_dict(l) for l in data.get("away_lineups", [])],
            home_coaches=data.get("home_coaches", "Unknown"),
            away_coaches=data.get("away_coaches", "Unknown"),
            events=[
                Events.from_dict(e)
                for e in safe_list(data.get("events"))
                if isinstance(e, dict)
            ],
        )