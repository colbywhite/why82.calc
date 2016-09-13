from unittest import TestCase

from nose.tools import *

import why82.tiers as tiers
from tests.utils import *


class TiersCalcTest(TestCase):
    def setUp(self):
        self.team_stats = get_json_resource('NBA_2016')

    def test_len(self):
        tier_info = tiers.calc(self.team_stats)
        eq_(len(tier_info), 30)

    def test_pace(self):
        tier_info = tiers.calc(self.team_stats)
        self.all_teams_contain(tier_info, 'pace')

    def test_win_loss(self):
        tier_info = tiers.calc(self.team_stats)
        self.all_teams_contain(tier_info, 'win_loss')

    def all_teams_contain(self, tier_info, key):
        for (k, v) in tier_info.iteritems():
            ok_(key in v)
