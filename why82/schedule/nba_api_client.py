import requests

NBA_SCOREBOARD_URL = 'http://stats.nba.com/stats/scoreboardV2'
NBA_LEAGUE_ID = '00'
NBA_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
NBA_API_HEADERS = {'Referer': 'http://stats.nba.com/scores/', 'User-Agent': NBA_USER_AGENT}

def v2scoreboard(start_date, offset):
    params = {'GameDate': start_date.strftime('%Y-%m-%d'), 'LeagueID': NBA_LEAGUE_ID, 'DayOffset': offset}
    print("hitting %s with params %s" % (NBA_SCOREBOARD_URL, params))
    response = requests.get(NBA_SCOREBOARD_URL, params=params, headers=NBA_API_HEADERS)
    print("received response")
    response.raise_for_status()
    return response.json()
