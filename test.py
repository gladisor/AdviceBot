import datetime
from utils import get_submissions, get_comments, get_data
import requests
import json

day = 1

after = int(datetime.datetime(2018, 1, day).timestamp())
before = int(datetime.datetime(2018, 1, day+1).timestamp())
new = datetime.datetime.fromtimestamp(after) + datetime.timedelta(days=1)

print(f'after {after}')
print(f'before {before}')
print(f'new {int(new.timestamp())}')

# sub = 'Advice'
#
# submissions = get_submissions(after, before, sub, size=5)
#
# get_data(submissions)
