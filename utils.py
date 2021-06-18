import requests
import json
import time
import itertools
import numpy as np
import pandas as pd

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

def get_data(after, before, sub):
    start = time.time()
    ## Querying submissions from pushshift
    submissions = get_submissions(after, before, sub, size=5)
    ## Filtering out submissions with less than one comment
    submissions = list(filter(lambda x: x['num_comments'] != 0, submissions))
    print('Querying and filtering submissions from pushshift: ', time.time()-start)

    ## Extracting id and question from each submission
    '''
    This step is a little complicated. What is happening here is:
        1.) "for sub in submissions" is iterating over each submission dictionary
            in the list.

        2.) "(sub['id'], sub['selftext'])" is taking out only the id and the text
            and packaging that into a tuple. This will result in a list of tuples

            [
            ('7z4st', 'Help my dog ate my homework! ...'),
            ...
            ('215zl', 'Blah Blah ....')
            ]

        3.) The "*" operator now disolves the list into a bunch of loose tuples
            which are now fed into the zip function.

        4.) The "zip" function takes two iterables and packages them together into units.
            For example if you have two lists:

            list1 = ['a', 'b', 'c']
            list2 = [1, 2, 3]

            and we call zip --> zip(list1, list2)
            it will produce --> [('a', 1), ('b', 2), ('c', 3)]

        5.) Finally we have a tuple of all the ids of the posts, and a tuple of all the
            text of the posts. In python there is multiple assignment so we assign
            variables "ids" and "questions" to the two tuples.
    '''

    start = time.time()
    # extract id and questions
    ids, questions = zip(*[(sub['id'], sub['selftext']) for sub in submissions])
    print('Extracting id and text: ', time.time()-start)

    start = time.time()
    # extract comments for each post id
    comments = list(map(get_comments, ids))
    print('Querying comments: ', time.time()-start)

    start = time.time()
    # extract number of comments 
    num_comments = list(map(len, comments))
    # chain comments into list 
    comments = list(itertools.chain(*comments))
    # extract text from comments 
    comments = [comment['body'] for comment in comments]
    print('Processing comments: ', time.time()-start)

    start = time.time()
    # storing questions 
    questions = np.array(questions, dtype=object)
    # iterating over number of comments 
    questions = np.repeat(questions, num_comments)
    print('Processing questions: ', time.time()-start)

    start = time.time()
    # output csv with questions and respective comments 
    data = pd.DataFrame({'question': questions, 'comment': comments})
    data.to_csv('small_data.csv')
    print('Saving data: ', time.time()-start)