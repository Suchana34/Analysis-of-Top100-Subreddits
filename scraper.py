import requests
from bs4 import BeautifulSoup
import praw
# praw is reddit api wrapper
from textblob import TextBlob
import math

url = requests.get("https://redditmetrics.com/top")

soup = BeautifulSoup(url.text, 'html.parser')

#to store them in a file
with open('sentiment.txt', 'w') as f:
    for subreddit in soup.find_all('a'):
        try:
            if '/r' in subreddit.string:
                f.write(subreddit.string[3:] + '\n')
        except:
            TypeError

# to find the sentiment in each comment
reddit = praw.Reddit(client_id = '', client_secret = '', user_agent = '')

with open('sentiment.txt', 'r') as f:

    #epoch timestamps

    day_start = 1589275924
    day_end = 1589535124
    
    for line in f:
        subreddit = reddit.subreddit(line.strip())

        sub_submissions = subreddit.submissions(day_start, day_end)

        sub_sentiments = 0
        num_comments = 0

        for submission in sub_submissions:
            if not submission.stickied: #to ignore the sticky posts on the top of subreddit
                # grab all the comments within that time range
                submission.comment.replace_more(limit = 0)
                # the above line grabs the comments from showmore as well
                for comment in submission.comments.list():
                    blob = TextBlob(comment.body)

                    comment_sentiment = blob.sentiment.polarity # positive or negative
                    sub_sentiments += comment_sentiment
                    num_comments += 1

        print('/r/' + str(subreddit.display.name))

        try:
            # calculate relative values
            print('ratio: ', str(math.floor(sub_sentiments/num_comments*100)) + '\n')
        except:
            print('No comment sentiment' + '\n')
            ZeroDivisionError
        
