import requests
import json
import time
import itertools
import numpy as np
import pandas as pd
import datetime

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

def get_submissions(after, before, subreddit, size=100):
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
        f'&subreddit={subreddit}'
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

def get_data(start_timestamp, subreddit):
    '''
    Pulls data from submissions and generates csv file containing
    questions and their respective answers.

    Parameters
    ----------
    start_timestamp : int
        Timestamp at which to collect one days worth of posts from.

    Returns
    -------
    DataFrame
        Pandas DataFrame object
    '''
    end_timestamp = datetime.datetime.fromtimestamp(start_timestamp) + datetime.timedelta(days=1)
    end_timestamp = int(end_timestamp.timestamp())
    ## Getting submissions from specified time and subreddit
    submissions = get_submissions(start_timestamp, end_timestamp, subreddit, 50)
    ## Extracting id and question from each submission
    ids, questions = zip(*[(sub['id'], sub['selftext']) for sub in submissions])
    # Extract comments for each post id
    comments = list(map(get_comments, ids))
    ## Filtering out non top level comments
    comments = list(map(
        lambda x: [item for item in x if item['link_id'] == item['parent_id']],
        comments
        ))

    # Extract number of comments
    num_comments = list(map(len, comments))
    # Chain comments into list
    comments = list(itertools.chain(*comments))
    # Extract text from comments
    comments = [comment['body'] for comment in comments]
    # Storing questions
    questions = np.array(questions, dtype=object)
    # Iterating over number of comments
    questions = np.repeat(questions, num_comments)
    # Output csv with questions and respective comments
    data = pd.DataFrame({'question': questions, 'comment': comments})
    return data
