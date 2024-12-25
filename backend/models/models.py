from datetime import datetime
from typing import Optional
from decouple import config
from sqlalchemy import TIMESTAMP, func, text
from sqlmodel import Field, SQLModel

class Base(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "nullable": True}
    )

class Team(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    team_id: int = Field(nullable=False)
    name: str = Field(default="Unnamed")

class Player(Base, table=True):
    player_id: int = Field(nullable=False)
    name: str = Field(default="Unnamed")
    position: str = Field(nullable=False)
    nfl_team: str = Field(nullable=False)

class Roster(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    team_id: int = Field(foreign_key="team.id", nullable=False)
    week: int = Field(nullable=False)
    player_id: int = Field(foreign_key="player.id", nullable=False)
    points: float = Field(default=0)
    projected_points: float = Field(default=0)

class Matchup(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    week: int = Field(nullable=False)
    home_id: int = Field(foreign_key="team.id", nullable=False)
    away_id: int = Field(foreign_key="team.id", nullable=False)
    home_points: float = Field(default=0)
    away_points: float = Field(default=0)
