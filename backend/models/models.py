from datetime import datetime
from typing import List, Optional
from decouple import config
from sqlalchemy import TIMESTAMP, func, text
from sqlmodel import Field, Relationship, SQLModel

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
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),  # Set to the current time on creation
            "onupdate": func.now(),  # Update to the current time on update
            "nullable": True
        }
    )

class Team(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    team_id: int = Field(nullable=False)
    team_name: str = Field(default="Unnamed")
    wins : int = Field(default=0)
    losses : int = Field(default=0)

    # Add relationships
    rosters: List["Roster"] = Relationship(back_populates="team")
    home_matchups: List["Matchup"] = Relationship(back_populates="home_team", sa_relationship_kwargs={'foreign_keys': '[Matchup.home_id]'})
    away_matchups: List["Matchup"] = Relationship(back_populates="away_team", sa_relationship_kwargs={'foreign_keys': '[Matchup.away_id]'})

class Player(Base, table=True):
    player_id: int = Field(nullable=False)
    name: str = Field(default="Unnamed")
    position: str = Field(nullable=False)
    nfl_team: str = Field(nullable=False)

    # Add relationships
    rosters: List["Roster"] = Relationship(back_populates="player")

class Roster(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    team_id: int = Field(foreign_key="team.id", nullable=False)
    week: int = Field(nullable=False)
    player_id: int = Field(foreign_key="player.player_id", nullable=False)
    points: float = Field(default=0)
    projected_points: float = Field(default=0)
    on_bench: bool = Field(default=False)

    # Add relationships
    team: Team = Relationship(back_populates="rosters")
    player: Player = Relationship(back_populates="rosters")

class Matchup(Base, table=True):
    league_id: int = Field(default=config('LEAGUE_ID'), nullable=False)
    year: int = Field(nullable=False)
    week: int = Field(nullable=False)
    home_id: int = Field(foreign_key="team.id", nullable=False)
    away_id: int = Field(foreign_key="team.id", nullable=False)
    home_points: float = Field(default=0, nullable=True)
    away_points: float = Field(default=0, nullable=True)
    home_projected: float = Field(default=0, nullable=True)
    away_projected: float = Field(default=0, nullable=True)

    # Add relationships
    home_team: Team = Relationship(back_populates="home_matchups", sa_relationship_kwargs={'foreign_keys': '[Matchup.home_id]'})
    away_team: Team = Relationship(back_populates="away_matchups", sa_relationship_kwargs={'foreign_keys': '[Matchup.away_id]'})
