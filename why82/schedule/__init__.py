from datetime import datetime

import requests

NBA_SCOREBOARD_URL = 'http://stats.nba.com/stats/scoreboardV2'
NBA_LEAGUE_ID = '00'
NBA_API_HEADERS = {'Referer': 'http://stats.nba.com/scores/', 'User-Agent': 'curl/7.43.0'}


def get_multi_day_schedule(start_date, num=7):
    return reduce(lambda result, offset:
                  dict(result.items() + get_schedule(start_date, offset).items()),
                  range(0, num), {})


def get_schedule(start_date, offset):
    params = {'GameDate': start_date.strftime('%Y-%m-%d'), 'LeagueID': NBA_LEAGUE_ID, 'DayOffset': offset}
    response = requests.get(NBA_SCOREBOARD_URL, params=params, headers=NBA_API_HEADERS)
    response.raise_for_status()
    game_strings = response.json()['resultSets'][0]['rowSet']
    date = parse_game_date(game_strings[0][5])
    games = map(lambda x: parse_game_teams(x[5]), game_strings)
    return {date: games}


def parse_game_teams(game_info):
    teams = game_info.split('/')[1]
    away_abbr = teams[:3]
    home_abbr = teams[3:]
    return {'home': home_abbr, 'away': away_abbr}


def parse_game_date(game_info):
    date_string = game_info.split('/')[0]
    return datetime.strptime(date_string, '%Y%m%d').date()
