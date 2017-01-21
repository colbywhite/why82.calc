import requests

NBA_SCOREBOARD_URL = 'http://stats.nba.com/stats/scoreboardV2'
NBA_LEAGUE_ID = '00'
NBA_API_HEADERS = {'Referer': 'http://stats.nba.com/scores/', 'User-Agent': 'curl/7.43.0'}


def v2scoreboard(start_date, offset):
    params = {'GameDate': start_date.strftime('%Y-%m-%d'), 'LeagueID': NBA_LEAGUE_ID, 'DayOffset': offset}
    print("hitting %s with params %s" % (NBA_SCOREBOARD_URL, params))
    response = requests.get(NBA_SCOREBOARD_URL, params=params, headers=NBA_API_HEADERS)
    print("received response")
    response.raise_for_status()
    return response.json()
