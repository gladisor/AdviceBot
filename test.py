import datetime
from utils import get_submissions, get_comments
import requests
import json
import itertools
import numpy as np
import pandas as pd

import time

day = 1
after = int(datetime.datetime(2018, 1, day).timestamp())
before = int(datetime.datetime(2018, 1, day+1).timestamp())
sub = 'Advice'
size = 10

start = time.time()
## Querying submissions from pushshift
submissions = get_submissions(after, before, sub, size=5)
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
ids, questions = zip(*[(sub['id'], sub['selftext']) for sub in submissions])
print('Extracting id and text: ', time.time()-start)

start = time.time()
## Getting list of lists of comments from each submission
comments = list(map(get_comments, ids))
print('Querying comments: ', time.time()-start)

start = time.time()
## Getting number of comments per post
num_comments = list(map(len, comments))
## Flattening comments into single list
comments = list(itertools.chain(*comments))
## Extracting the text from each comment
comments = [comment['body'] for comment in comments]
print('Processing comments: ', time.time()-start)

start = time.time()
## Storing questions in a numpy array so we can use the repeat function
questions = np.array(questions, dtype=object)
## Repeating the question for the number of comments that it has
questions = np.repeat(questions, num_comments)
print('Processing questions: ', time.time()-start)

start = time.time()
## Combining the questions with their respective comments
data = pd.DataFrame({'question': questions, 'comment': comments})
data.to_csv('small_data.csv')
print('Saving data: ', time.time()-start)
