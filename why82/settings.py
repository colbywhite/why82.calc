import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BUCKET_NAME = os.environ.get('BUCKET_NAME')
CURRENT_SEASON = os.environ.get('CURRENT_SEASON')
VERSION = '0.2'
