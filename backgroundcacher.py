import praw
import random
import time
import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url)

MAXMEMORY = "30mb"
POLICY = 'allkeys-lru'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def fetch_and_cache_meme(subreddit_name):
    cache_key = f'subreddit:{subreddit_name}'
    subreddit = reddit.subreddit(subreddit_name)
    submissions = list(subreddit.hot(limit=50))
    memes = [
        {
            'title': submission.title,
            'url': submission.url,
            'permalink': submission.permalink
        }
        for submission in submissions
    ]
    r.setex(cache_key, 300, json.dumps(memes))

def update_caches(top_subreddits):
    for subreddit in top_subreddits:
        fetch_and_cache_meme(subreddit)
        time.sleep(random.randint(5, 10))

top_subreddits = ["memes", "dankmemes", "funny", "wholesome", "nobodyasked"]
while True:
    seed = int(time.time() * 1000) % 1000
    random.seed(time.time())
    update_caches(top_subreddits)
    time.sleep(2)

