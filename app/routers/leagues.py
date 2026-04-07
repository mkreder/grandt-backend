import string, random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import League, LeagueMember, User
from app.schemas.schemas import LeagueCreate, LeagueJoin, LeagueOut, LeagueMemberOut
from app.services.auth import get_current_user

router = APIRouter(prefix="/leagues", tags=["leagues"])


def _generate_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@router.post("/", response_model=LeagueOut, status_code=201)
def create_league(data: LeagueCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    code = _generate_code()
    while db.query(League).filter(League.code == code).first():
        code = _generate_code()
    league = League(name=data.name, code=code, owner_id=user.id)
    db.add(league)
    db.flush()
    db.add(LeagueMember(league_id=league.id, user_id=user.id))
    db.commit()
    db.refresh(league)
    return _league_out(league, db)


@router.post("/join", response_model=LeagueOut)
def join_league(data: LeagueJoin, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    league = db.query(League).filter(League.code == data.code.upper()).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    if db.query(LeagueMember).filter(LeagueMember.league_id == league.id, LeagueMember.user_id == user.id).first():
        raise HTTPException(status_code=400, detail="Already a member")
    db.add(LeagueMember(league_id=league.id, user_id=user.id))
    db.commit()
    db.refresh(league)
    return _league_out(league, db)


@router.get("/", response_model=list[LeagueOut])
def my_leagues(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    memberships = db.query(LeagueMember).filter(LeagueMember.user_id == user.id).all()
    leagues = [db.query(League).filter(League.id == m.league_id).first() for m in memberships]
    return [_league_out(l, db) for l in leagues if l]


@router.get("/{league_id}", response_model=LeagueOut)
def get_league(league_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return _league_out(league, db)


def _league_out(league: League, db: Session) -> LeagueOut:
    members = db.query(LeagueMember).filter(LeagueMember.league_id == league.id).all()
    member_outs = []
    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        if user:
            member_outs.append(LeagueMemberOut(id=user.id, username=user.username))
    return LeagueOut(id=league.id, name=league.name, code=league.code, owner_id=league.owner_id, members=member_outs)
