from copy import deepcopy
from datetime import datetime

import nba_api_client as nba

ABBREVIATION_ADJUSTMENTS = {'PHX': 'PHO', 'CHA': 'CHO', 'BKN': 'BRK'}
INCORRECT_ABBREVIATIONS = ABBREVIATION_ADJUSTMENTS.keys()


def get_multi_day_schedule(start_date, num=7):
    return reduce(lambda result, offset:
                  dict(result.items() + get_single_day_schedule(start_date, offset).items()),
                  range(0, num), {})


def get_single_day_schedule(start_date, offset):
    game_strings = nba.v2scoreboard(start_date, offset)['resultSets'][0]['rowSet']
    if len(game_strings) == 0:
        return {}
    date = parse_game_date(game_strings[0][5])
    games = map(lambda x: parse_game_teams(x[5]), game_strings)
    return {date: games}


def parse_game_teams(game_info):
    teams = game_info.split('/')[1]
    away_abbr = correct_abbreviations(teams[:3])
    home_abbr = correct_abbreviations(teams[3:])
    return {'home': home_abbr, 'away': away_abbr}


def parse_game_date(game_info):
    date_string = game_info.split('/')[0]
    return datetime.strptime(date_string, '%Y%m%d').date()


def correct_abbreviations(abbr):
    if abbr in INCORRECT_ABBREVIATIONS:
        return ABBREVIATION_ADJUSTMENTS[abbr]
    return abbr


def grade_schedule(schedule, tiers):
    result = {}
    for day in schedule.keys():
        graded_games = []
        for game in schedule[day]:
            home_abbrev = game['home']
            away_abbrev = game['away']
            graded_game = {'home': deepcopy(tiers[home_abbrev]),
                           'away': deepcopy(tiers[away_abbrev])}
            graded_game['home']['abbreviated_name'] = home_abbrev
            graded_game['away']['abbreviated_name'] = away_abbrev
            graded_game['grade'] = grade_game(graded_game)
            graded_games.append(graded_game)
        formatted_day = day.strftime('%Y-%m-%d')
        result[formatted_day] = graded_games
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
