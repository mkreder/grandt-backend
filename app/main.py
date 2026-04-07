from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, players, match_days, teams, leagues, standings

app = FastAPI(title="GranDT Mundial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(players.router)
app.include_router(match_days.router)
app.include_router(teams.router)
app.include_router(leagues.router)
app.include_router(standings.router)


@app.get("/health")
def health():
    return {"status": "ok"}
