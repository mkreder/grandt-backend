"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-07
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
    )

    op.create_table(
        "players",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("country", sa.String, nullable=False),
        sa.Column("position", sa.Enum("arquero", "defensor", "mediocampista", "delantero", name="position_enum"), nullable=False),
    )

    op.create_table(
        "match_days",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("deadline", sa.DateTime, nullable=False),
    )

    op.create_table(
        "player_scores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("player_id", sa.Integer, sa.ForeignKey("players.id"), nullable=False),
        sa.Column("match_day_id", sa.Integer, sa.ForeignKey("match_days.id"), nullable=False),
        sa.Column("goals", sa.Integer, default=0),
        sa.Column("assists", sa.Integer, default=0),
        sa.Column("yellow_cards", sa.Integer, default=0),
        sa.Column("red_cards", sa.Integer, default=0),
        sa.Column("clean_sheet", sa.Boolean, default=False),
        sa.Column("own_goals", sa.Integer, default=0),
        sa.Column("minutes_played", sa.Integer, default=0),
        sa.Column("total_points", sa.Float, default=0),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), unique=True, nullable=False),
    )

    op.create_table(
        "team_players",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("player_id", sa.Integer, sa.ForeignKey("players.id"), nullable=False),
    )

    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("code", sa.String(6), unique=True, nullable=False, index=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )

    op.create_table(
        "league_members",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("league_id", sa.Integer, sa.ForeignKey("leagues.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_table("league_members")
    op.drop_table("leagues")
    op.drop_table("team_players")
    op.drop_table("teams")
    op.drop_table("player_scores")
    op.drop_table("match_days")
    op.drop_table("players")
    op.drop_table("users")
