from datetime import datetime
from functools import cache
from fastapi import HTTPException

from backend.helpers.ttl_cache import ttl_cache

from .models.models import Team

from .database.database import Database
from .handlers.espn_api import EspnAPI
from espn_api.football import BoxScore, BoxPlayer

SECONDS_IN_A_DAY = 60 * 60 * 24

@ttl_cache(SECONDS_IN_A_DAY)
def league_teams() -> dict[int, str]:
    espn_api = EspnAPI()
    league_teams = espn_api.get_league_teams()
    league_team_id_and_name = {team.team_id : team.team_name.strip() for team in league_teams}
    return league_team_id_and_name

@ttl_cache(SECONDS_IN_A_DAY)
def points_per_position_per_week(team_id):
    espn_api = EspnAPI()

    current_week = espn_api.get_current_week()

    points_per_position = {}

    for week in range(1, current_week):

        points_per_position_per_week = {}

        box_scores = espn_api.get_week_box_score(week)
        lineup = team_lineup_from_boxscores(tuple(box_scores), team_id)
        
        for player in lineup:
            points_per_position_per_week[player.position] = round(points_per_position_per_week.get(player.position, 0) + player.points, 2)

        points_per_position[week] = points_per_position_per_week


    return points_per_position

@cache
def team_lineup_from_boxscores(box_scores : tuple[BoxScore], team_id) -> list[BoxPlayer]:
    lineup = None

    try:
        team_id = int(team_id)
    except Exception as ex:
        print(f'ID: {team_id} cannot be casted to an int')
        raise HTTPException(status_code=404, detail=f'ID: {team_id} cannot be casted to an int')
    
    for bs in box_scores:
        if team_id == bs.home_team.team_id:
            lineup = bs.home_lineup
        elif team_id == bs.away_team.team_id:
            lineup = bs.away_lineup

    if lineup is None:
        print(f'Matchup for Team with ID {team_id} not found')
        raise HTTPException(status_code=404, detail=f'Matchup for Team with ID {team_id} not found')
    
    return lineup

def test_db():
    Database().save(Team(created_at=datetime.now(), year=2024, team_id=1, name='Sams Team'))

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

@cache
def points_on_bench_for_team_on_week(team_id, week):
    box_scores = EspnAPI().get_week_box_score(week)
    lineup = team_lineup_from_boxscores(tuple(box_scores), team_id)
    return points_on_bench_for_lineup(lineup)


def points_on_bench_for_lineup(lineup : tuple[BoxPlayer]):
    points = 0
    
    for player in lineup:
        if player.lineupSlot == 'BE':
            points += player.points
    
    return points