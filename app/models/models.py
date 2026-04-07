import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Position(str, enum.Enum):
    GK = "arquero"
    DEF = "defensor"
    MID = "mediocampista"
    FWD = "delantero"


SCORING_RULES = {
    "goal": {Position.FWD: 3, Position.MID: 4, Position.DEF: 5, Position.GK: 5},
    "assist": 2,
    "clean_sheet": {Position.GK: 3, Position.DEF: 1, Position.MID: 0, Position.FWD: 0},
    "yellow_card": -1,
    "red_card": -3,
    "own_goal": -2,
    "played": 1,
}


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    position = Column(Enum(Position, values_callable=lambda x: [e.value for e in x], name="position_enum", create_type=False), nullable=False)


class MatchDay(Base):
    __tablename__ = "match_days"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)


class PlayerScore(Base):
    __tablename__ = "player_scores"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    match_day_id = Column(Integer, ForeignKey("match_days.id"), nullable=False)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    clean_sheet = Column(Boolean, default=False)
    own_goals = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    total_points = Column(Float, default=0)

    player = relationship("Player")
    match_day = relationship("MatchDay")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    players = relationship("TeamPlayer", back_populates="team")
    user = relationship("User")


class TeamPlayer(Base):
    __tablename__ = "team_players"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    team = relationship("Team", back_populates="players")
    player = relationship("Player")


class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String(6), unique=True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    members = relationship("LeagueMember", back_populates="league")
    owner = relationship("User")


class LeagueMember(Base):
    __tablename__ = "league_members"
    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    league = relationship("League", back_populates="members")
    user = relationship("User")
