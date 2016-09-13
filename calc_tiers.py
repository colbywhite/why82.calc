import argparse
from datetime import date as _date
from datetime import datetime

import simplejson as json

from why82.s3_recorder import S3Recorder
import why82.tiers as tiers


def calc_tiers(stats):
    return json.dumps(tiers.calc(stats))


def save_tiers(save_date, stats):
    tier_json = calc_tiers(stats)
    S3Recorder.record(save_date, tier_json)


def date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate team tiers based on stats')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'), help='File to read stats from')
    parser.add_argument('--s3', action='store_true', help='Save the results to S3. Otherwise print results')
    parser.add_argument('--date', '-d', default=_date.today(), type=date, help='The date to save the tier info as. '
                                                                               'DEFAULT=date.today()')
    args = parser.parse_args()
    stats_input = json.loads(args.file.read())
    if args.s3:
        save_tiers(args.date, stats_input)
    else:
        print(calc_tiers(stats_input))
