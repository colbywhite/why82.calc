import os
from datetime import datetime
import simplejson as json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def load_season_info(name):
    file_name = "%s.json" % name
    file_path = os.path.join(os.path.dirname(__file__), 'seasons', file_name)
    with open(file_path, 'r') as f:
        info = json.loads(f.read())
    info['start'] = datetime.strptime(info['start'], '%Y-%m-%d').date()
    info['end'] = datetime.strptime(info['end'], '%Y-%m-%d').date()
    return info

BUCKET_NAME = os.environ.get('BUCKET_NAME')
CURRENT_SEASON = load_season_info(os.environ.get('CURRENT_SEASON'))
VERSION = '0.2'
