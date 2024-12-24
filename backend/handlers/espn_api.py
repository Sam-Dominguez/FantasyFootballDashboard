from espn_api.football import League, Team
from decouple import config

class EspnAPI(object):
    _instance = None

    league : League = None

    def __new__(self):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(EspnAPI, self).__new__(self)
            
            self.league = League(
                league_id=config('LEAGUE_ID'),
                year=int(config('YEAR')),
                espn_s2=config('ESPN_S2'),
                swid=config('SWID')
            )

        return self._instance
    
    def get_league_teams(self) -> list[Team]:
        return self.league.teams
    
    