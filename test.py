import datetime
from utils import get_submissions, get_comments
import requests
import json
import itertools
import numpy as np
import pandas as pd

after = int(datetime.datetime(2018, 1, 3).timestamp())
before = int(datetime.datetime(2018, 1, 4).timestamp())
sub = 'Advice'
size = 5

## Querying submissions from pushshift
submissions = get_submissions(after, before, sub, size)
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
ids, questions = zip(*[(sub['id'], sub['selftext']) for sub in submissions])

## Getting list of lists of comments from each submission
comments = list(map(get_comments, ids))
## Getting number of comments per post
num_comments = list(map(len, comments))
## Flattening comments into single list
comments = list(itertools.chain(*comments))
## Extracting the text from each comment
comments = [comment['body'] for comment in comments]

## Storing questions in a numpy array so we can use the repeat function
questions = np.array(questions, dtype=object)
## Repeating the question for the number of comments that it has
questions = np.repeat(questions, num_comments)

## Combining the questions with their respective comments
data = pd.DataFrame({'question':questions, 'comment':comments})
print(data)
