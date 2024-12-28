from backend.helpers.middleware import get_league_teams, get_roster
from backend.helpers.ttl_cache import ttl_cache
from backend.models.models import Roster

from .database.database import Database
from .handlers.espn_api import EspnAPI
from espn_api.football import BoxPlayer

SECONDS_IN_A_DAY = 60 * 60 * 24

@ttl_cache(SECONDS_IN_A_DAY)
def league_teams() -> dict[int, str]:
    league_teams = get_league_teams()
    league_team_id_and_name = {team.team_id : team.team_name.strip() for team in league_teams}
    return league_team_id_and_name

def points_per_position_per_week(team_id):
    current_week = EspnAPI().get_current_week()

    points_per_position = {}

    for week in range(1, current_week):

        points_per_position_per_week = {}

        roster = get_roster(team_id, week)
        
        for player in roster:
            points_per_position_per_week[player.player.position] = round(points_per_position_per_week.get(player.player.position, 0) + player.points, 2)

        points_per_position[week] = points_per_position_per_week


    return points_per_position

def test_db():
    return Database().get_league_teams()

def points_on_bench():
    teams = league_teams()

    points_on_bench = {name : points_on_bench_for_team(id) for id, name in teams.items()}
    average_pob = sum(points_on_bench.values()) / len(points_on_bench)

    return {"teams" : points_on_bench, "average" : average_pob}

def points_on_bench_for_team(team_id):

    current_week = EspnAPI().get_current_week()

    points_on_bench = 0

    for week in range(1, current_week):
        points_on_bench += points_on_bench_for_team_on_week(team_id, week)

    return round(points_on_bench, 2)

def points_on_bench_for_team_on_week(team_id, week):
    lineup = get_roster(team_id, week)
    return points_on_bench_for_roster(lineup)


def points_on_bench_for_roster(roster : list[Roster]):
    points = 0
    
    for player in roster:
        if player.on_bench:
            points += player.points
    
    return points

def win_percentages():
    league_teams = get_league_teams()
    return {team.team_id : round(team.wins / (team.losses + team.wins), 3) for team in league_teams}
