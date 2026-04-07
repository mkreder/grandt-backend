from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import MatchDay, PlayerScore, Player, User
from app.schemas.schemas import MatchDayCreate, MatchDayOut, PlayerScoreCreate, PlayerScoreOut
from app.services.auth import require_admin, get_current_user
from app.services.scoring import calculate_points

router = APIRouter(prefix="/match-days", tags=["match_days"])


@router.get("/", response_model=list[MatchDayOut])
def list_match_days(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(MatchDay).order_by(MatchDay.deadline).all()


@router.post("/", response_model=MatchDayOut, status_code=201)
def create_match_day(data: MatchDayCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    md = MatchDay(**data.model_dump())
    db.add(md)
    db.commit()
    db.refresh(md)
    return md


@router.post("/{match_day_id}/scores", response_model=list[PlayerScoreOut], status_code=201)
def add_scores(
    match_day_id: int,
    scores: list[PlayerScoreCreate],
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    md = db.query(MatchDay).filter(MatchDay.id == match_day_id).first()
    if not md:
        raise HTTPException(status_code=404, detail="Match day not found")
    results = []
    for s in scores:
        player = db.query(Player).filter(Player.id == s.player_id).first()
        if not player:
            raise HTTPException(status_code=404, detail=f"Player {s.player_id} not found")
        ps = PlayerScore(match_day_id=match_day_id, **s.model_dump())
        ps.total_points = calculate_points(ps, player.position)
        db.add(ps)
        results.append(ps)
    db.commit()
    for r in results:
        db.refresh(r)
    return results


@router.get("/{match_day_id}/scores", response_model=list[PlayerScoreOut])
def get_scores(match_day_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(PlayerScore).filter(PlayerScore.match_day_id == match_day_id).all()
