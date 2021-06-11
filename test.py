import datetime
from utils import get_submissions, get_comments
import requests
import json

after = int(datetime.datetime(2018, 1, 3).timestamp())
before = int(datetime.datetime(2018, 1, 4).timestamp())
sub = 'Advice'
size = 5

submissions = get_submissions(after, before, sub, size)

for submission in submissions:
    f = open(submission['id'] + '.txt', 'w', encoding='utf-8')
    f.write('Query:\n')
    f.write(submission['selftext'])
    f.write('\n\n')

    comments = get_comments(submission['id'])

    if len(comments) > 0:
        comments = filter(lambda x: x['link_id'] == x['parent_id'], comments)

        for comment in comments:
            print(comment['body'])
            f.write('Response:\n')
            f.write(comment['body'])
            f.write('\n\n')
    f.close()
