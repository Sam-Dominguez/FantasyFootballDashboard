from datetime import datetime, timedelta
from backend.database.database import Database
from backend.database.db_helper import update_league_teams, save_matchup, save_roster
from backend.handlers.espn_api import EspnAPI
from backend.models.models import Matchup, Roster
from espn_api.football import BoxPlayer, BoxScore

ONE_DAY_AGO = datetime.now() - timedelta(days=1)

def get_league_teams():
    teams_from_db = Database().get_league_teams()

    if len(teams_from_db) > 0 and all(team.updated_at > ONE_DAY_AGO for team in teams_from_db):
        print('League teams are fresh, returning from database')
        return teams_from_db  # Data is fresh; return from DB
    else:
        print('League teams are stale, returning from ESPN API')
        teams_from_api = EspnAPI().get_league_teams()
        update_league_teams(EspnAPI().league, teams_from_api)
        return teams_from_api
    
def get_box_scores(week : int) -> list[Matchup]:
    matchups = Database().get_matchups_on_week(week)

    if len(matchups) > 1:
        print('Matchups found in database, returning from db')
    else:
        print('Matchups not found in database, fetching from ESPN API')
        box_scores = EspnAPI().get_week_box_score(week)
        save_matchup(EspnAPI().league, box_scores, week)
        matchups = Database().get_matchups_on_week(week)
    
    return matchups
    
def get_roster(team_id : int, week : int) -> list[Roster]:
        
    players = Database().get_roster_on_week(team_id, week)

    if len(players) > 1:
        print('Roster found in database, returning from db')
    else:
        print('Roster not found in database, fetching from ESPN API')
        box_score_players = team_lineup_from_boxscores(EspnAPI().get_week_box_score(week), team_id)
        save_roster(EspnAPI().league, box_score_players, week, team_id)
        players = Database().get_roster_on_week(team_id, week)
    
    return players
    
def team_lineup_from_boxscores(box_scores : tuple[BoxScore], team_id) -> list[BoxPlayer]:
    lineup = None

    try:
        team_id = int(team_id)
    except Exception as ex:
        print(f'ID: {team_id} cannot be casted to an int')
        return
    
    for bs in box_scores:
        if team_id == bs.home_team.team_id:
            lineup = bs.home_lineup
        elif team_id == bs.away_team.team_id:
            lineup = bs.away_lineup

    if lineup is None:
        print(f'Matchup for Team with ID {team_id} not found')
        return
    
    return lineup