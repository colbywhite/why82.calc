import requests
from datetime import datetime
from datetime import timedelta
import pytz

# TODO: replace this junk with something more reliable.
NBA_SCOREBOARD_URL = 'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2016/league/00_full_schedule.json'
NBA_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
NBA_API_HEADERS = {'User-Agent': NBA_USER_AGENT, 'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, sdch'}
ABBREVIATION_ADJUSTMENTS = {'PHX': 'PHO', 'CHA': 'CHO', 'BKN': 'BRK'}
INCORRECT_ABBREVIATIONS = ABBREVIATION_ADJUSTMENTS.keys()

class ScheduleRetriever(object):
    def __init__(self, start_date):
        self.start_date = start_date
        self._cached_sked = None

    def __call__(self, offset):
        new_date = self.start_date + timedelta(days=offset)
        return self.day_sked(new_date)

    def cached_sked(self):
        if not self._cached_sked:
            self._cached_sked = full_sked()
        return self._cached_sked

    def month_sked(self, date):
        month_name = date.strftime('%B')
        full = self.cached_sked()['lscd']
        filtered_for_month = filter(lambda x: x['mscd']['mon']==month_name, full)
        return filtered_for_month[0]['mscd']['g']

    def day_sked(self, date):
        month_games = self.month_sked(date)
        day = date.strftime('%Y-%m-%d')
        raw_sked = filter(lambda x: x['gdte']==day, month_games)
        return map(lambda x: self.format_game(x), raw_sked)

    def format_game(self, game):
        return {
            'home': self.correct_abbreviations(game['h']['ta']),
            'away': self.correct_abbreviations(game['v']['ta']),
            'nat_tv': self.parse_nat_tv(game['bd']['b']),
            'time': self.parse_utc_time(game['gdtutc'], game['utctm']),
            'gdte': game['gdte']
        }

    def parse_utc_time(self, date_str, time_str):
        date_time_str = date_str + ' ' + time_str
        tz_naive = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        return pytz.utc.localize(tz_naive)


    def parse_nat_tv(self, broadcasters):
        broadcaster = filter(lambda x: (x['type']=='tv' and x['scope']=='natl'), broadcasters)
        if broadcaster:
            return broadcaster[0]['disp']
        else:
            return None

    def correct_abbreviations(self, abbr):
        if abbr in INCORRECT_ABBREVIATIONS:
            return ABBREVIATION_ADJUSTMENTS[abbr]
        return abbr


def full_sked():
    print("hitting %s" % (NBA_SCOREBOARD_URL))
    response = requests.get(NBA_SCOREBOARD_URL, headers=NBA_API_HEADERS)
    print("received response")
    response.raise_for_status()
    return response.json()

def multi_day_sked(date, num_days):
    results = map(ScheduleRetriever(date), range(0, num_days))
    return reduce(lambda r, single_day:
                    dict(r.items() + dict([(single_day[0]['gdte'], single_day)]).items()),
                    results, {})
