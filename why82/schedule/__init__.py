from datetime import datetime

import nba_api_client as nba

ABBREVIATION_ADJUSTMENTS = {'PHX': 'PHO', 'CHA': 'CHO', 'BKN': 'BRK'}
INCORRECT_ABBREVIATIONS = ABBREVIATION_ADJUSTMENTS.keys()


def get_multi_day_schedule(start_date, num=7):
    return reduce(lambda result, offset:
                  dict(result.items() + get_schedule(start_date, offset).items()),
                  range(0, num), {})


def get_schedule(start_date, offset):
    game_strings = nba.v2scoreboard(start_date, offset)['resultSets'][0]['rowSet']
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
