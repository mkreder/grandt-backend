from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.models import Position


# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool
    model_config = {"from_attributes": True}


# Players
class PlayerCreate(BaseModel):
    name: str
    country: str
    position: Position

class PlayerOut(BaseModel):
    id: int
    name: str
    country: str
    position: Position
    model_config = {"from_attributes": True}


# Match Days
class MatchDayCreate(BaseModel):
    name: str
    deadline: datetime

class MatchDayOut(BaseModel):
    id: int
    name: str
    deadline: datetime
    model_config = {"from_attributes": True}


# Player Scores
class PlayerScoreCreate(BaseModel):
    player_id: int
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    clean_sheet: bool = False
    own_goals: int = 0
    minutes_played: int = 0

class PlayerScoreOut(BaseModel):
    id: int
    player_id: int
    match_day_id: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    clean_sheet: bool
    own_goals: int
    minutes_played: int
    total_points: float
    model_config = {"from_attributes": True}


# Teams
class TeamSet(BaseModel):
    player_ids: list[int]

class TeamPlayerOut(BaseModel):
    id: int
    name: str
    country: str
    position: Position
    model_config = {"from_attributes": True}

class TeamOut(BaseModel):
    id: int
    user_id: int
    players: list[TeamPlayerOut]
    model_config = {"from_attributes": True}


# Leagues
class LeagueCreate(BaseModel):
    name: str

class LeagueJoin(BaseModel):
    code: str

class LeagueMemberOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}

class LeagueOut(BaseModel):
    id: int
    name: str
    code: str
    owner_id: int
    members: list[LeagueMemberOut]
    model_config = {"from_attributes": True}


# Standings
class StandingEntry(BaseModel):
    user_id: int
    username: str
    total_points: float
    points_by_match_day: dict[str, float]
