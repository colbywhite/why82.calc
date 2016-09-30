import argparse
from datetime import date as _date
from datetime import datetime

import simplejson as json

import why82.schedule as sked
from why82.s3_recorder import S3Recorder
import why82.settings as settings
import why82.utils as utils


# noinspection PyUnusedLocal
def lambda_handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    start_date = datetime.strptime(key,'2016/%Y-%m-%d-tiers.json').date()
    season = settings.load_season_info(key.split('/')[0])
    tiers = S3Recorder.load_json_file(key)
    print('Saving 7-day schedule starting on %s' % start_date)
    save_schedule(start_date, 7, season, tiers)


def calc_schedule(start_date, num):
    return sked.get_multi_day_schedule(start_date, num)


def grade_schedule(start_date, num, tiers):
    schedule = calc_schedule(start_date, num)
    return json.dumps(sked.grade_schedule(schedule, tiers))


def save_schedule(start_date, num, season, tiers):
    schedule_json = grade_schedule(start_date, num, tiers)
    file_name = utils.build_file_name(start_date, season, 'schedule')
    S3Recorder.record(file_name, schedule_json)


def date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


if __name__ == '__main__':
    default_season_name = int(settings.CURRENT_SEASON['name'])
    season_help = 'The season to save the tiers in. DEFAULT=%s' % default_season_name
    date_help = 'The start date of the generated schedule. DEFAULT=date.today()'
    amount_help = 'The number of days to get a schedule for, starting with START_DATE. DEFAULT=1'

    parser = argparse.ArgumentParser(description='Generate a schedule with tier information')
    parser.add_argument('tiers', type=argparse.FileType('r'), help='The file to use for tier information')
    parser.add_argument('--amount', '-a', default=1, type=int, help=amount_help)
    parser.add_argument('--s3', action='store_true', help='Save the results to S3. Otherwise print results')
    parser.add_argument('--date', '-d', metavar='START_DATE', default=_date.today(), type=date, help=date_help)
    parser.add_argument('--season', '-s', default=default_season_name, type=int, help=season_help)

    args = parser.parse_args()
    tiers_input = json.loads(args.tiers.read())

    if args.s3:
        season_info = settings.load_season_info(args.season)
        save_schedule(args.date, args.amount, season_info, tiers_input)
    else:
        print(grade_schedule(args.date, args.amount, tiers_input))
