from fastapi import HTTPException
from handlers.espn_api import EspnAPI
from espn_api.football import Team, BoxScore, BoxPlayer


def get_league_teams():
    espn_api = EspnAPI()
    league_teams = espn_api.get_league_teams()
    league_team_id_and_name = {team.team_id : team.team_name.strip() for team in league_teams}
    return league_team_id_and_name

def get_points_per_position_per_week(team_id):
    espn_api = EspnAPI()

    current_week = espn_api.get_current_week()

    points_per_position = {}

    for week in range(1, current_week):

        points_per_position_per_week = {}

        box_scores = espn_api.get_week_box_score(week)
        lineup = get_team_lineup_from_boxscores(box_scores, team_id)
        
        for player in lineup:
            points_per_position_per_week[player.position] = round(points_per_position_per_week.get(player.position, 0) + player.points, 2)

        points_per_position[week] = points_per_position_per_week


    return points_per_position

def get_team_lineup_from_boxscores(box_scores : list[BoxScore], team_id) -> list[BoxPlayer]:

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
        