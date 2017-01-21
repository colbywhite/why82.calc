from copy import deepcopy
from datetime import datetime
import pytz
import nba_api_client as nba
# using a ThreadPool since a regular Pool doesn't work on AWS lambda
from multiprocessing.pool import ThreadPool

ABBREVIATION_ADJUSTMENTS = {'PHX': 'PHO', 'CHA': 'CHO', 'BKN': 'BRK'}
INCORRECT_ABBREVIATIONS = ABBREVIATION_ADJUSTMENTS.keys()
EASTERN = pytz.timezone('US/Eastern')

class ScheduleRetriever(object):
    def __init__(self, start_date):
        self.start_date = start_date
    def __call__(self, offset):
        return get_single_day_schedule(self.start_date, offset)


def get_multi_day_schedule(start_date, num=7):
    p = ThreadPool(num)
    results = p.map(ScheduleRetriever(start_date), range(0,num))
    p.close()
    return reduce(lambda r, single_day:
                  dict(r.items() + single_day.items()),
                  results, {})


def get_single_day_schedule(start_date, offset):
    game_strings = nba.v2scoreboard(start_date, offset)['resultSets'][0]['rowSet']
    if len(game_strings) == 0:
        return {}
    date = parse_game_date(game_strings[0][5])
    games = map(lambda x: parse_game_teams(date, x), game_strings)
    return {date: games}


def parse_game_teams(date, game_info):
    teams = game_info[5].split('/')[1]
    away_abbr = correct_abbreviations(teams[:3])
    home_abbr = correct_abbreviations(teams[3:])
    time = parse_eastern_time(date, game_info[4]).strftime('%Y-%m-%dT%H:%M:%S%z')
    nat_tv = parse_national_tv(game_info[11])
    return {'home': home_abbr, 'away': away_abbr, 'time': time, "nat_tv": nat_tv}

def parse_eastern_time(date, human_time_str):
    time_str = date.strftime('%Y-%m-%d ') + human_time_str
    tz_naive = datetime.strptime(time_str, '%Y-%m-%d %I:%M %p ET')
    return EASTERN.localize(tz_naive)

def parse_national_tv(human_tv_string):
    if human_tv_string:
        return human_tv_string.strip().replace(' ', '').lower()
    else:
        return None

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
        print('Grading schedule for day %s' % day)
        graded_games = []
        for game in schedule[day]:
            home_abbrev = game['home']
            away_abbrev = game['away']
            graded_game = {'home': deepcopy(tiers[home_abbrev]),
                           'away': deepcopy(tiers[away_abbrev]),
                           'time': game['time'],
                           'nat_tv': game['nat_tv']}
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
