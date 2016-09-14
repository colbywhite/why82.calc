import requests

NBA_SCOREBOARD_URL = 'http://stats.nba.com/stats/scoreboardV2'
NBA_LEAGUE_ID = '00'
NBA_API_HEADERS = {'Referer': 'http://stats.nba.com/scores/', 'User-Agent': 'curl/7.43.0'}


def get_seven_day_schedule(start_date):
    return {get_schedule(start_date, n) for n in range(0, 6)}


def get_schedule(start_date, offset):
    params = {'GameDate': start_date.strftime('%Y-%m-%d'), 'LeagueID': NBA_LEAGUE_ID, 'DayOffset': offset}
    response = requests.get(NBA_SCOREBOARD_URL, params=params, headers=NBA_API_HEADERS)
    response.raise_for_status()
    games = response.json()['resultSets'][0]['rowSet']
    return {game[5] for game in games}
