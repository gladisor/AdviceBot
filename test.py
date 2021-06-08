import datetime
from utils import get_submissions, request_data
import pandas as pd
import requests
import json

after = int(datetime.datetime(2019, 1, 1).timestamp())
before = int(datetime.datetime(2019, 1, 2).timestamp())
sub = 'Advice'
size = 5

submissions = get_submissions(after, before, sub, size)

data = pd.DataFrame(submissions)

post_id = data['id'][0]

url = f'https://api.pushshift.io/reddit/submission/comment_ids/{post_id}'

comment_ids = request_data(url)
comment_ids = ','.join(comment_ids)

url = (
    f'https://api.pushshift.io/reddit/search/comment/'
    f'?ids={comment_ids}'
    )

comments = request_data(url)

print(comments)
