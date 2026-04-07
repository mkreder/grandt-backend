from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Team, TeamPlayer, Player, MatchDay, User, Position
from app.schemas.schemas import TeamSet, TeamOut, TeamPlayerOut
from app.services.auth import get_current_user

router = APIRouter(prefix="/teams", tags=["teams"])

REQUIRED_FORMATION = {Position.GK: 1, Position.DEF: 4, Position.MID: 3, Position.FWD: 3}


@router.put("/", response_model=TeamOut)
def set_team(data: TeamSet, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check deadline of next match day
    next_md = db.query(MatchDay).filter(MatchDay.deadline > datetime.now(timezone.utc)).order_by(MatchDay.deadline).first()
    if next_md and datetime.now(timezone.utc) > next_md.deadline.replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=400, detail="Deadline passed")

    if len(data.player_ids) != 11:
        raise HTTPException(status_code=400, detail="Must select exactly 11 players")
    if len(set(data.player_ids)) != 11:
        raise HTTPException(status_code=400, detail="Duplicate players")

    players = db.query(Player).filter(Player.id.in_(data.player_ids)).all()
    if len(players) != 11:
        raise HTTPException(status_code=400, detail="Some players not found")

    # Validate formation
    pos_count = {}
    for p in players:
        pos_count[p.position] = pos_count.get(p.position, 0) + 1
    if pos_count != REQUIRED_FORMATION:
        raise HTTPException(status_code=400, detail=f"Invalid formation. Required: {REQUIRED_FORMATION}")

    team = db.query(Team).filter(Team.user_id == user.id).first()
    if team:
        db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).delete()
    else:
        team = Team(user_id=user.id)
        db.add(team)
        db.flush()

    for pid in data.player_ids:
        db.add(TeamPlayer(team_id=team.id, player_id=pid))
    db.commit()
    db.refresh(team)
    return _team_out(team)


@router.get("/", response_model=TeamOut)
def get_my_team(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    team = db.query(Team).filter(Team.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="No team set")
    return _team_out(team)


def _team_out(team: Team) -> TeamOut:
    return TeamOut(
        id=team.id,
        user_id=team.user_id,
        players=[TeamPlayerOut(id=tp.player.id, name=tp.player.name, country=tp.player.country, position=tp.player.position) for tp in team.players],
    )
