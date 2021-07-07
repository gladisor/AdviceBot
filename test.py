import datetime
from utils import get_submissions, get_comments, get_data
import requests
import json

subreddit = 'Advice'

success = 0
failure = 0

start_timestamp = int(datetime.datetime(2019, 1, 3).timestamp())
data = get_data(start_timestamp, subreddit)
print(data)

# for day in range(1, 30):
#     start_timestamp = int(datetime.datetime(2018, 1, day).timestamp())
#     try:
#         data = get_data(start_timestamp, subreddit)
#         success += 1
#
#     except Exception as e:
#         failure += 1
#
#     print(f'Success: {success}, Failure: {failure}')
