from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import League, LeagueMember, Team, TeamPlayer, PlayerScore, MatchDay, User
from app.schemas.schemas import StandingEntry
from app.services.auth import get_current_user

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/{league_id}", response_model=list[StandingEntry])
def get_standings(league_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    members = db.query(LeagueMember).filter(LeagueMember.league_id == league_id).all()
    match_days = db.query(MatchDay).order_by(MatchDay.deadline).all()

    standings = []
    for member in members:
        user = db.query(User).filter(User.id == member.user_id).first()
        team = db.query(Team).filter(Team.user_id == member.user_id).first()
        if not user or not team:
            continue

        player_ids = [tp.player_id for tp in db.query(TeamPlayer).filter(TeamPlayer.team_id == team.id).all()]
        total = 0.0
        by_md = {}
        for md in match_days:
            scores = db.query(PlayerScore).filter(
                PlayerScore.match_day_id == md.id,
                PlayerScore.player_id.in_(player_ids),
            ).all()
            md_pts = sum(s.total_points for s in scores)
            by_md[md.name] = md_pts
            total += md_pts

        standings.append(StandingEntry(user_id=user.id, username=user.username, total_points=total, points_by_match_day=by_md))

    standings.sort(key=lambda x: x.total_points, reverse=True)
    return standings
