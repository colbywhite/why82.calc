import argparse
from datetime import date as _date
from datetime import datetime

import simplejson as json

from why82.s3_recorder import S3Recorder
import why82.tiers as tiers
import why82.settings as settings
import why82.utils as utils


def lambda_handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    season = settings.load_season_info(key.split('/')[0])
    key_template = '%s/%%Y-%%m-%%d-stats.json' % season['name']
    save_date = datetime.strptime(key,key_template).date()
    stats = S3Recorder.load_json_file(key, settings.STATS_BUCKET_NAME)
    print('Saving tiers for %s' % save_date)
    save_tiers(save_date, stats, season)


def calc_tiers(stats):
    return json.dumps(tiers.calc(stats))


def save_tiers(save_date, stats, season):
    tier_json = calc_tiers(stats)
    file_name = utils.build_file_name(save_date, season, 'tiers')
    S3Recorder.record(file_name, tier_json)


def date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


if __name__ == '__main__':
    default_season_name = int(settings.CURRENT_SEASON['name'])
    season_help = 'The season to save the tiers in. DEFAULT=%s' % default_season_name
    date_help = 'The date to save the tiers for. DEFAULT=date.today()'

    parser = argparse.ArgumentParser(description='Calculate team tiers based on stats')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'), help='File to read stats from')
    parser.add_argument('--s3', action='store_true', help='Save the results to S3. Otherwise print results')
    parser.add_argument('--season', '-s', default=default_season_name, type=int, help=season_help)
    parser.add_argument('--date', '-d', default=_date.today(), type=date, help=date_help)

    args = parser.parse_args()
    stats_input = json.loads(args.file.read())
    if args.s3:
        season_info = settings.load_season_info(args.season)
        save_tiers(args.date, stats_input, season_info)
    else:
        print(calc_tiers(stats_input))
