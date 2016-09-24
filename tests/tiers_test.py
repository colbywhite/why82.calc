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
        self.overall_tier_info = overall.calc_overall(self.tier_info)

    def test_load_weight_config(self):
        weights, total_weight = overall.load_weight_config()
        eq_(total_weight, 40)
        eq_(weights['pace'], 10)
        eq_(weights['win_loss'], 20)
        eq_(weights['rating_diff'], 10)

    def test_weighted_avg(self):
        eq_(Decimal('1.25'), self.overall_tier_info['TOR']['overall']['avg'])
        eq_(Decimal('1.25'), self.overall_tier_info['BOS']['overall']['avg'])
        eq_(Decimal('1.75'), self.overall_tier_info['MIA']['overall']['avg'])
        eq_(Decimal('1.5'), self.overall_tier_info['ATL']['overall']['avg'])
        eq_(Decimal('.75'), self.overall_tier_info['GSW']['overall']['avg'])
        eq_(Decimal('2.25'), self.overall_tier_info['MIL']['overall']['avg'])

    def test_weighted_tier(self):
        eq_(Decimal('1'), self.overall_tier_info['TOR']['overall']['tier'])
        eq_(Decimal('1'), self.overall_tier_info['BOS']['overall']['tier'])
        eq_(Decimal('2'), self.overall_tier_info['MIA']['overall']['tier'])
        eq_(Decimal('1'), self.overall_tier_info['ATL']['overall']['tier'])
        eq_(Decimal('1'), self.overall_tier_info['GSW']['overall']['tier'])
        eq_(Decimal('2'), self.overall_tier_info['MIL']['overall']['tier'])
