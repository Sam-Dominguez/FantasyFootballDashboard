from espn_api.football import Team, League, BoxScore, BoxPlayer
from backend.models.models import Player, Roster, Team as FBTeam
from backend.models.models import Matchup
from .database import Database

def save_league_teams(league : League, teams : list[Team]):
    print(f'Saving {len(teams)} league teams')
    Database().save([convert_team_object(league, team) for team in teams])

def update_league_teams(league : League, teams : list[Team]):
    print(f'Updating {len(teams)} league teams')
    Database().update([convert_team_object(league, team) for team in teams])

def convert_team_object(league : League, team : Team) -> FBTeam:
    return FBTeam(
            team_id=team.team_id,
            league_id=league.league_id,
            year=league.year,
            team_name=team.team_name,
            wins=team.wins,
            losses=team.losses
    )

def save_matchup(league : League, box_scores : list[BoxScore], week : int):
    print(f'Saving {len(box_scores)} matchups')
    Database().save([convert_matchup_object(league, matchup, week) for matchup in box_scores])

def convert_matchup_object(league : League, box_score : BoxScore, week : int) -> Matchup:
    return Matchup(
            league_id=league.league_id,
            year=league.year,
            week=week,
            home_id=box_score.home_team.team_id,
            away_id=box_score.away_team.team_id,
            home_points=box_score.home_score,
            away_points=box_score.away_score,
            home_projected=box_score.home_projected,
            away_projected=box_score.away_projected,
    )

def save_roster(league : League, box_players : list[BoxPlayer], week : int, team_id : int):

    players_to_save = []
    rosters_to_save = []

    for box_player in box_players:
        player = Database().get_player(box_player.playerId)
        if player is None:
            print(f'{box_player.name} not in database, adding to save list.')
            players_to_save.append(convert_player_object(box_player))
        else:
            print(f'{box_player.name} in database, skipping...')

    rosters_to_save.extend([convert_roster_object(league, box_player, week, team_id) for box_player in box_players])

    print(f'Saving {len(players_to_save)} players and {len(rosters_to_save)} rosters...')
    Database().save(players_to_save + rosters_to_save)

def convert_roster_object(league : League, box_player : BoxPlayer, week : int, team_id : int) -> Roster:
    return Roster(
            league_id=league.league_id,
            year=league.year,
            week=week,
            team_id=team_id,
            player_id=box_player.playerId,
            points=box_player.points,
            projected_points=box_player.projected_points,
            on_bench=box_player.lineupSlot == 'BE'
    )

def convert_player_object(box_player : BoxPlayer) -> Player:
    return Player(
            player_id=box_player.playerId,
            name=box_player.name,
            position=box_player.position,
            nfl_team=box_player.proTeam
    )