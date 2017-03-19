from copy import deepcopy
from datetime import datetime
import pytz
from nba_api_client import multi_day_sked

def grade_schedule(schedule, tiers):
    result = {}
    for day in schedule.keys():
        print('Grading schedule for day %s' % day)
        graded_games = []
        for game in schedule[day]:
            print('Grading game for day %s' % game)
            home_abbrev = game['home']
            away_abbrev = game['away']
            if home_abbrev != 'WST' or away_abbrev != 'EST':
                graded_game = {'home': deepcopy(tiers[home_abbrev]),
                               'away': deepcopy(tiers[away_abbrev]),
                               'time': game['time'].strftime('%Y-%m-%dT%H:%M:%S%z'),
                               'nat_tv': game['nat_tv']}
                graded_game['home']['abbreviated_name'] = home_abbrev
                graded_game['away']['abbreviated_name'] = away_abbrev
                graded_game['grade'] = grade_game(graded_game)
                graded_games.append(graded_game)
        result[day] = graded_games
    return result


def grade_game(game):
    home_pace_tier = game['home']['overall']['tier']
    away_tier = game['away']['overall']['tier']
    if home_pace_tier == 3 or away_tier == 3:
        return 'D'
    elif home_pace_tier == 1 and away_tier == 1:
        return 'A'
    elif home_pace_tier == 2 and away_tier == 2:
        return 'C'
    else:
        # these are 2v1 games
        return 'B'
