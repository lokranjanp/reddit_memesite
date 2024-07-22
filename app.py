from flask import Flask, render_template
import praw
import random
import os
import redis
import json

app = Flask(__name__)   # initialised new flask app
MAXMEMORY = "30mb"
POLICY = 'allkeys-lru'

# loading .env credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

# creating the praw object.
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Setup Redis connection
redis_url = os.getenv('REDISCLOUD_URL')
r = redis.from_url(redis_url)

r.config_set('maxmemory', MAXMEMORY)
r.config_set('maxmemory-policy', POLICY)


def get_random_meme(subreddit_name):
    cached_submissions = r.get(f'subreddit:{subreddit_name}')
    if cached_submissions:
        submissions = json.loads(cached_submissions)
    else:
        subreddit = reddit.subreddit(subreddit_name)  # fetch subreddit
        submissions = [{
            'title': submission.title,
            'url': submission.url,
            'permalink': submission.permalink
        } for submission in subreddit.hot(limit=690)]  # fetch memes
        r.setex(f'subreddit:{subreddit_name}', 300, json.dumps(submissions))  # Cache for 5 minutes

    submission = random.choice(submissions)  # choose random meme
    return submission


@app.route('/')
def home():
    meme = get_random_meme('dankmemes')
    return render_template('index.html', meme=meme, countdown=30)


if __name__ == '__main__':
    app.run(debug=True)
