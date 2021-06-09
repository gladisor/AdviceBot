import datetime
from utils import get_submissions, get_comments
import pandas as pd
import requests
import json

after = int(datetime.datetime(2019, 1, 1).timestamp())
before = int(datetime.datetime(2019, 1, 2).timestamp())
sub = 'Advice'
size = 5

submissions = get_submissions(after, before, sub, size)

data = pd.DataFrame(submissions)
print(data)

post_id = data['id'][0]
print(post_id)

comments = get_comments(post_id)

print(len(comments))
