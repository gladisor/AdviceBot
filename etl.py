import json
import praw
from utils import is_helpful

# keys = json.load(open('keys.json'))
#
# reddit = praw.Reddit(
#     client_id=keys['client_id'],
#     client_secret=keys['client_secret'],
#     user_agent='AdviceBot')

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

# sub = reddit.subreddit('advice').search('flair:"Advice Received"')
#
# print(len(list(sub)))

from pmaw import PushshiftAPI
import datetime


if __name__ == '__main__':
    import inspect
    api = PushshiftAPI()

    start_time = int(datetime.datetime(2019, 1, 1).timestamp())

    print(inspect.signature(api.search_submissions))
    #
    # posts = api.search_submissions(
    #     after=start_time,
    #     subreddit='Advice',
    #     # q='Advice Received',
    #     limit=10)
    #
    # for post in posts:
    #     for item in post.items():
    #         print(item)
    #     break
    #     print(post['id'])
    #
    #     if post['num_comments'] > 0:
    #
    #         ids = api.search_submission_comment_ids(
    #             ids=post['id'],
    #             limit=100)
    #
    #         comments = api.search_comments(ids=ids)
    #
    #         post_id = post['id']
    #         print(f'Post id: {post_id}')
    #
    #         ## if comment['author'] == 'AdviceFlairBot'
    #
    #         for comment in comments:
    #             parent_id = comment['parent_id']
    #             comment_id = comment['id']
    #             link_id = comment['link_id']
    #
    #             distinguished = comment['distinguished']
    #             author = comment['author']
    #
    #             print(f'Distinguished: {distinguished}')
    #             print(f'Author: {author}')
    #             print(\
    #                 f'Parent id: {parent_id},\
    #                 Comment id: {comment_id},\
    #                 Link id: {link_id}')
