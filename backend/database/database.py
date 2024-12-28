from decouple import config
from sqlalchemy import Engine
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, Session, create_engine, select
from backend.models.models import *

sqlite_file_name = config('DB_FILENAME')
sqlite_url = f"sqlite:///{sqlite_file_name}"

class Database():
    _instance = None

    engine : Engine = None

    def __new__(self):
        if self._instance is None:
            print('Creating database object')
            self._instance = super(Database, self).__new__(self)
            
            self.engine = create_engine(sqlite_url, echo=False)
            SQLModel.metadata.create_all(self.engine)

        return self._instance
    
    def save(self, record):

        session = Session(self.engine)

        if isinstance(record, list):
            session.add_all(record)
        else:
            session.add(record)

        session.commit()

        session.close()
        
        print('Saved.')

    def update(self, record):
        session = Session(self.engine)

        if isinstance(record, list):
            # iterable
            for rec in record:
                session.merge(rec)
        else:
            # not iterable
            session.merge(record)

        session.commit()
        print('Updated.')
        session.close()

    def delete(self, record):
        session = Session(self.engine)

        if isinstance(record, list):
            # iterable
            for rec in record:
                session.add(rec)
        else:
            # not iterable
            session.add(record)

        session.commit()
        print('Deleted.')
        session.close()

    def get_league_teams(self) -> list[Team]:
        session = Session(self.engine)

        statement = select(Team).where(
            Team.league_id == config('LEAGUE_ID'), 
            Team.year == config('YEAR')
        )

        result = session.exec(statement)

        teams = result.all()

        session.close()

        return teams
    
    def get_matchups_on_week(self, week) -> list[Matchup]:
        session = Session(self.engine)

        statement = select(Matchup).where(
            Matchup.league_id == config('LEAGUE_ID'), 
            Matchup.year == config('YEAR'),
            Matchup.week == week
        )

        result = session.exec(statement)

        return result.all()
    
    def get_roster_on_week(self, team_id : int, week : int) -> list[Roster]:
        session = Session(self.engine)

        statement = select(Roster).join(Player).where(
            Roster.league_id == config('LEAGUE_ID'), 
            Roster.year == config('YEAR'),
            Roster.week == week,
            Roster.team_id == team_id
        ).options(selectinload(Roster.player))

        result = session.exec(statement)

        roster = result.all()

        session.close()

        return roster
    
    def get_player(self, player_id : int) -> Optional[Player]:

        session = Session(self.engine)

        statement = select(Player).where(
            Player.player_id == player_id
        )

        result = session.exec(statement)

        player = result.first()

        session.close()

        return player

