from handlers.espn_api import EspnAPI


def get_league_teams():
    espn_api = EspnAPI()
    league_teams = espn_api.get_league_teams()
    league_teams_names = list(map(lambda x: x.team_name.strip(), league_teams))
    return league_teams_names