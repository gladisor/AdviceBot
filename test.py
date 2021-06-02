import datetime
from utils import get_submissions

after = int(datetime.datetime(2019, 1, 1).timestamp())
before = int(datetime.datetime(2019, 1, 2).timestamp())
sub = 'Advice'
size = 85
min_comments = 3

submissions = get_submissions(after, before, sub, size, min_comments)

for post in submissions:
    print(post['title'], '\n')

print(len(submissions))
