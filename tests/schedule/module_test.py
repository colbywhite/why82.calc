from datetime import date, timedelta
from decimal import Decimal
from unittest import TestCase

from nose.tools import *

import tests.utils as utils
import why82.schedule as sked
import why82.schedule.nba_api_client as nba


class GetScheduleTest(TestCase):
    def v2scoreboard(self, start_date, offset):
        name = 'NBA_scoreboardv2_%s_%d' % (start_date.strftime('%Y-%m-%d'), offset)
        return utils.get_json_resource(name)

    def setUp(self):
        nba.v2scoreboard = self.v2scoreboard

    def test_get_single_day_schedule(self):
        schedule = sked.get_single_day_schedule(date(2016, 2, 3), 1)
        dates = schedule.keys()
        eq_(len(dates), 1)
        day = dates[0]
        eq_(day, date(2016, 2, 4))
        games = schedule[day]
        eq_(len(games), 4)
        expected_games = utils.get_json_resource('NBA_schedule_2016-02-03_1')
        eq_(games, expected_games)

    def test_get_multi_day_schedule(self):
        start_date = date(2016, 2, 3)
        schedule = sked.get_multi_day_schedule(start_date, 3)
        dates = schedule.keys()
        eq_(len(dates), 3)
        eq_(set(dates), {date(2016, 2, 5), date(2016, 2, 4), start_date})
        for day in dates:
            offset = day - start_date
            name = 'NBA_schedule_%s_%d' % (start_date.strftime('%Y-%m-%d'), offset.days)
            games = schedule[day]
            expected_games = utils.get_json_resource(name)
            eq_(games, expected_games)


class GradeScheduleTest(TestCase):
    def setUp(self):
        # build three days of schedule
        start_date = date(2016, 2, 3)
        self.date_strings = []
        self.schedule = {}
        for offset in range(0, 3):
            cur_date = start_date + timedelta(days=offset)
            self.date_strings.append(cur_date.strftime('%Y-%m-%d'))
            name = 'NBA_schedule_%s_%d' % (start_date.strftime('%Y-%m-%d'), offset)
            self.schedule[cur_date] = utils.get_json_resource(name)
        self.tiers = utils.get_json_resource('NBA_2016-tiers')
        self.graded_schedule = sked.grade_schedule(self.schedule, self.tiers)

    def test_game_counts(self):
        eq_(11, len(self.graded_schedule['2016-02-03']))
        eq_(4, len(self.graded_schedule['2016-02-04']))
        eq_(10, len(self.graded_schedule['2016-02-05']))

    def test_game_contents(self):
        games = self.graded_schedule['2016-02-04']
        game = [g for g in games if g['home']['abbreviated_name'] == 'DET']
        eq_(1, len(game))
        game = game[0]
        eq_('DET', game['home']['abbreviated_name'])
        eq_('NYK', game['away']['abbreviated_name'])
        eq_(3, game['home']['pace']['tier'])
        eq_(Decimal('95.1'), game['home']['pace']['pace'])
        eq_(3, game['away']['pace']['tier'])
        eq_(Decimal('93.4'), game['away']['pace']['pace'])
