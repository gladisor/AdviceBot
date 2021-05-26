import requests
import json
import datetime

after = str(int(datetime.datetime(2019, 1, 1).timestamp()))
before = str(int(datetime.datetime(2019, 2, 1).timestamp()))
sub = 'Advice'

print(after)
print(before)

url = f'https://api.pushshift.io/reddit/search/submission/?after={after}$before={before}&subreddit={sub}&size={100}'

r = requests.get(url)
print(r)
data = json.loads(r.text)

print(data)
