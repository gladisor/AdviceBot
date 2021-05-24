import json
import praw
from utils import is_helpful

keys = json.load(open('keys.json'))

reddit = praw.Reddit(
    client_id=keys['client_id'],
    client_secret=keys['client_secret'],
    user_agent='AdviceBot')

# submission = reddit.submission('njsm1e')
#
# helpful_comments = []
# for comment in submission.comments:
#     helpful = is_helpful(comment)
#     print(comment.ups, helpful)
#     if helpful:
#         helpful_comments.append(comment.body)
#
# print(helpful_comments)

sub = reddit.subreddit('advice').search('flair:"Advice Received"')

print(len(list(sub)))

# for flair in sub.flair.templates:
#     print(flair)
