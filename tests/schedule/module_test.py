from datetime import date, timedelta
from decimal import Decimal
from unittest import TestCase

from nose.tools import *

from tests.utils import get_json_resource
import why82.schedule as sked

class GradeScheduleTest(TestCase):
    def setUp(self):
        # build three days of schedule
        start_date = date(2016, 2, 3)
        self.schedule = {}
        for offset in range(0, 3):
            cur_date = start_date + timedelta(days=offset)
            name = 'NBA_schedule_%s_%d' % (start_date.strftime('%Y-%m-%d'), offset)
            self.schedule[cur_date] = get_json_resource(name)
        self.tiers = get_json_resource('NBA_2016-tiers')
        self.graded_schedule = sked.grade_schedule(self.schedule, self.tiers)

    def test_game_counts(self):
        eq_(11, len(self.graded_schedule['2016-02-03']))
        eq_(4, len(self.graded_schedule['2016-02-04']))
        eq_(10, len(self.graded_schedule['2016-02-05']))

    # def test_game_contents(self):
        # expected_schedule = get_json_resource('2016-02-03-schedule')
        # eq_(expected_schedule, self.graded_schedule)

    def test_grade_a_grading(self):
        game = self.get_single_game('CLE', '2016-02-05')
        eq_(1, game['home']['overall']['tier'])
        eq_(1, game['away']['overall']['tier'])
        eq_('A', game['grade'])

    def test_grade_b_grading(self):
        game = self.get_single_game('CHO', '2016-02-03')
        eq_(2, game['home']['overall']['tier'])
        eq_(1, game['away']['overall']['tier'])
        eq_('B', game['grade'])

    def test_grade_c_grading(self):
        game = self.get_single_game('CHO', '2016-02-05')
        eq_(2, game['home']['overall']['tier'])
        eq_(2, game['away']['overall']['tier'])
        eq_('C', game['grade'])

    def get_single_game(self, home_abbrev, date_string):
        games = self.graded_schedule[date_string]
        game = [g for g in games if g['home']['abbreviated_name'] == home_abbrev]
        eq_(1, len(game))
        return game[0]
