import json
import praw

keys = json.load(open('keys.json'))

reddit = praw.Reddit(
    client_id=keys['client_id'],
    client_secret=keys['client_secret'],
    user_agent='AdviceBot')

for submission in reddit.subreddit('advice').search('flair:"Advice Received"', limit=1):
    print(submission.author)
    print(submission.title)
    print(submission.selftext)
    for comment in submission.comments[0:5]:
        print(comment.body)
