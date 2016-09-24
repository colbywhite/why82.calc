from unittest import TestCase

from nose.tools import *
from decimal import Decimal

import why82.tiers as tiers
import why82.tiers.overall as overall
from tests.utils import get_json_resource


class TiersCalcTest(TestCase):
    def setUp(self):
        self.team_stats = get_json_resource('NBA_2016')
        self.tier_info = tiers.calc(self.team_stats)

    def test_len(self):
        eq_(len(self.tier_info), 30)

    def test_pace(self):
        self.all_teams_contain(self.tier_info, 'pace')

    def test_win_loss(self):
        self.all_teams_contain(self.tier_info, 'win_loss')

    def all_teams_contain(self, tier_info, key):
        for (k, v) in tier_info.iteritems():
            ok_(key in v)


class OverallTiersTest(TestCase):
    def setUp(self):
        self.tier_info = get_json_resource('NBA_2016-tiers')

    def test_load_weight_config(self):
        weights, total_weight = overall.load_weight_config()
        eq_(total_weight, 30)
        eq_(weights['pace'], 10)
        eq_(weights['win_loss'], 20)

    def test_weighted_avg(self):
        result = overall.calc_overall(self.tier_info)
        eq_(Decimal('1.667'), result['TOR']['overall']['avg'])
        eq_(Decimal('1.667'), result['BOS']['overall']['avg'])
        eq_(Decimal('2.333'), result['MIA']['overall']['avg'])
        eq_(Decimal('2'), result['ATL']['overall']['avg'])
        eq_(Decimal('1'), result['GSW']['overall']['avg'])
        eq_(Decimal('3'), result['MIL']['overall']['avg'])
