from unittest import TestCase
from tests.utils import get_json_resource
from datetime import datetime
from nose.tools import *
import pytz
import simplejson as json

import why82.schedule.nba_api_client as nba

class NBAAPIClientTest(TestCase):
    def full_sked(self):
        # TODO assert this is only called once
        return get_json_resource('full_schedule')

    def setUp(self):
        nba.full_sked = self.full_sked

    def test_multi_day_sked(self):
        start_date = datetime(2017, 03, 31)
        result = nba.multi_day_sked(start_date, 2)
        eq_(len(result),  2)
        eq_(len(result['2017-03-31']),  11)
        eq_(result['2017-03-31'][1]['home'], 'CHO')
        eq_(result['2017-03-31'][1]['away'], 'DEN')
        eq_(result['2017-03-31'][8]['nat_tv'], 'ESPN')
        eq_(result['2017-03-31'][7]['nat_tv'], None)
        eq_(result['2017-03-31'][4]['time'], pytz.utc.localize(datetime(2017, 4, 1, 0, 0)))
        eq_(result['2017-03-31'][9]['time'], pytz.utc.localize(datetime(2017, 4, 1, 1, 0)))
        eq_(len(result['2017-04-01']), 5)
