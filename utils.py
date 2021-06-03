import requests
import json

def get_submissions(after, before, sub, size=100, min_comments=3):
    '''
    Function which gets submissions from the pushshift api.

    Parameters
    ----------
    after : int
        Integer unix timestamp for the start date to the desired window
    before : int
        Integer unix timestamp for the end date to the desired window
    sub : str
        Name of the subreddit to get submissions from
    size : int (optional)
        Number of posts to grab (100 maximum)
    min_comments : int
        Minimum number of comments required for a post to be returned

    Returns
    -------
    list
        Submissions which match the search criteria.
    '''
    url = (
        f'https://api.pushshift.io/reddit/search/submission/'
        f'?after={after}'
        f'&before={before}'
        f'&subreddit={sub}'
        f'&size={size}'
        f'&num_comments>={min_comments}'
        )

    r = requests.get(url)
    data = json.loads(r.text)

    return data['data']

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
