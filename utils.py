import requests
import json

def request_data(url):
    '''
    Uses requests library to pull data from a url

    Parameters
    ----------
    url : str
        URL from which to gather data

    Returns
    -------
    dict
        Dictionary response from request
    '''

    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def get_submissions(after, before, sub, size=100):
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
        )

    return request_data(url)

def get_comments(submission_id):
    '''
    Gets comments from a given submission id.

    Parameters
    ----------
    submission_id : str
        Base 36 id which identifies a post

    Returns
    -------
    list
        List of dicts containing comment data
    '''
    url = f'https://api.pushshift.io/reddit/search/comment/?link_id={submission_id}'

    return request_data(url)

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
