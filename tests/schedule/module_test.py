from datetime import date
from unittest import TestCase

from nose.tools import *

import tests.utils as utils
import why82.schedule.nba_api_client as nba
import why82.schedule as sked


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
