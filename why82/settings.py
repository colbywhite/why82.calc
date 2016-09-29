import os
import simplejson as json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def load_season_info(name):
    file_name = "%s.json" % name
    file_path = os.path.join(os.path.dirname(__file__), 'seasons', file_name)
    with open(file_path, 'r') as f:
        return json.loads(f.read())

BUCKET_NAME = os.environ.get('BUCKET_NAME')
CURRENT_SEASON = load_season_info(os.environ.get('CURRENT_SEASON'))
VERSION = '0.2'
