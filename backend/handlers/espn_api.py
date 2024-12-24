from espn_api.football import League, Team, BoxScore, Player
from decouple import config
from fastapi import HTTPException

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
    
    def get_league_team(self, team_id) -> Team:
        teams : list[Team] = self.get_league_teams()

        try:
            team_id = int(team_id)
        except Exception as ex:
            print(f'ID: {team_id} cannot be casted to an int')
            raise HTTPException(status_code=404, detail=f'ID: {team_id} cannot be casted to an int')

        teams_ = [team for team in teams if team.team_id == team_id]

        if len(teams_) == 0:
            print(f'Team with ID {team_id} not found')
            raise HTTPException(status_code=404, detail=f'Team with ID {team_id} not found')
        
        if len(teams_) > 1:
            print(f'Multiple teams with ID {team_id} found')
            raise HTTPException(status_code=404, detail=f'Multiple teams with ID {team_id} found') 
        
        return teams_[0]
    
    def get_current_week(self) -> int:
        return self.league.current_week
    
    def get_week_box_score(self, week_num) -> list[BoxScore]:
        return self.league.box_scores(week_num)
    
    def get_player_infos(self, player_ids) -> list[Player]:
        return self.league.player_info(playerId=player_ids)
    
    