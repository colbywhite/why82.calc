import argparse
from datetime import date as _date
from datetime import datetime

import why82.schedule as sked


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    calc_schedule(_date.today())


def calc_schedule(start_date):
    return sked.get_seven_day_schedule(start_date)


def calc_schedule_offset(start_date, offset):
    return sked.get_schedule(start_date, offset)


def date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a day\'s schedule with tier information')
    parser.add_argument('--offset', '-o', default=0, type=int, help='The offset from the start date. DEFAULT=0')
    parser.add_argument('--date', '-d', default=_date.today(), type=date, help='The start date to grab a schedule for. '
                                                                               'DEFAULT=date.today()')
    args = parser.parse_args()
    # print(calc_schedule_offset(args.date, args.offset))
    print(calc_schedule(args.date))
