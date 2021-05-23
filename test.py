import json
import praw

keys = json.load(open('keys.json'))

reddit = praw.Reddit(
    client_id=keys['client_id'],
    client_secret=keys['client_secret'],
    user_agent='AdviceBot')

submission = reddit.submission('njdouc')
# print(submission.link_flair_text) ## prints Advice Received

def is_helpful(comment):
    '''
    Recursively searches comment trees to see if the root comment
    is marked by OP as helpful.

    Parameters
    ----------
    comment : Comment
        A praw Comment object, praw.models.reddit.comment.Comment

    Returns
    -------
    bool
        True if the given comment was helpful otherwise false.
    '''
    helpful = True if comment.distinguished else False

    for reply in comment.replies:
        helpful = is_helpful(reply)

    return helpful

for comment in submission.comments:
    print(comment.__class__)
    # helpful = is_helpful(comment)
    # print(comment.ups, helpful)

# for submission in reddit.subreddit('advice').search('flair:"Advice Received"', limit=1):
#     print(submission.author)
#     print(submission.title)
#     print(submission.selftext)
#     for comment in submission.comments[0:5]:
#         print(comment.body)
