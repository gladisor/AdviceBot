import requests
import json
import datetime

after = int(datetime.datetime(2019, 1, 1).timestamp())
before = int(datetime.datetime(2019, 10, 1).timestamp())
sub = 'Advice'

print(after)
print(before)
# nlt18t
# url = f'https://api.pushshift.io/reddit/search/submission/?after={after}$before={before}&subreddit={sub}&size={100}'
url = f'https://api.pushshift.io/reddit/search/submission/?q=Advice%Recived&after={after}&before={before}&subreddit=Advice&size={1000}'
# q=flair_name%3A%22Advice%Recived%22&restrict_sr=1
r = requests.get(url)
data = json.loads(r.text)

for post in data['data']:
    print(post['title'])
