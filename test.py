import datetime
from utils import get_submissions, get_comments, get_data
import requests
import json

day = 1

after = int(datetime.datetime(2018, 1, day).timestamp())
before = int(datetime.datetime(2018, 1, day+1).timestamp())
sub = 'Advice'

get_data(after, before, sub)