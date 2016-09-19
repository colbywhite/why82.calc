import argparse
from datetime import date as _date
from datetime import datetime

import simplejson as json

import why82.schedule as sked
from why82.s3_recorder import S3Recorder


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    calc_schedule(_date.today(), 7)


def calc_schedule(start_date, num):
    return sked.get_multi_day_schedule(start_date, num)


def grade_schedule(start_date, num, tiers):
    schedule = calc_schedule(start_date, num)
    schedule_json = json.dumps(sked.grade_schedule(schedule, tiers))
    S3Recorder.record(start_date, 'schedule', schedule_json)


def date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a day\'s schedule with tier information')
    parser.add_argument('tiers', type=argparse.FileType('r'), help='The file to use for tier information')
    parser.add_argument('--amount', '-a', default=1, type=int,
                        help='The number of days to get a schedule for, starting with START_DATE. DEFAULT=1')
    parser.add_argument('--date', '-d', metavar='START_DATE', default=_date.today(), type=date,
                        help='The start date to grab a schedule for. DEFAULT=date.today()')
    args = parser.parse_args()
    tiers_input = json.loads(args.tiers.read())
    print(grade_schedule(args.date, args.amount, tiers_input))
