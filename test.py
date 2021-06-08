import datetime
from utils import get_submissions
import pandas as pd

after = int(datetime.datetime(2019, 1, 1).timestamp())
before = int(datetime.datetime(2019, 1, 2).timestamp())
sub = 'Advice'

submissions = get_submissions(after, before, sub)
#
# for post in submissions:
#     print(post['title'], '\n')
#
# print(len(submissions))

data = pd.DataFrame(submissions)

print(data)
