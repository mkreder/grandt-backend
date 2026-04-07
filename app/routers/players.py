from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Player, User
from app.schemas.schemas import PlayerCreate, PlayerOut
from app.services.auth import require_admin, get_current_user

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[PlayerOut])
def list_players(
    country: str | None = Query(None),
    position: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(Player)
    if country:
        q = q.filter(Player.country == country)
    if position:
        q = q.filter(Player.position == position)
    return q.all()


@router.post("/", response_model=PlayerOut, status_code=201)
def create_player(data: PlayerCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    player = Player(**data.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.post("/bulk", response_model=list[PlayerOut], status_code=201)
def create_players_bulk(data: list[PlayerCreate], db: Session = Depends(get_db), _: User = Depends(require_admin)):
    players = [Player(**p.model_dump()) for p in data]
    db.add_all(players)
    db.commit()
    for p in players:
        db.refresh(p)
    return players


@router.delete("/{player_id}", status_code=204)
def delete_player(player_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
