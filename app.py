from flask import Flask, render_template, request
import praw
import threading
import time
import random
import os
import redis
import json

app = Flask(__name__)   # Initialised new Flask app
MAXMEMORY = "30mb"
POLICY = 'allkeys-lru'

# Loading .env credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

# Creating the PRAW object
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Setup Redis connection
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url)

top_subreddits = ['dankmemes', 'memes', 'wholesomememes', 'funny', 'nsfw']

def fetch_and_cache_meme(subreddit_name):
    cache_key = f'subreddit:{subreddit_name}'
    subreddit = reddit.subreddit(subreddit_name)
    submissions = list(subreddit.hot(limit=690))
    memes = [
        {
            'title': submission.title,
            'url': submission.url,
            'permalink': submission.permalink
        }
        for submission in submissions
    ]
    r.setex(cache_key, 300, json.dumps(memes))  # Cache for 5 minutes

def update_caches():
    threads = []
    for subreddit in top_subreddits:
        thread = threading.Thread(target=fetch_and_cache_meme, args=(subreddit,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def schedule_cache_updates():
    while True:
        update_caches()
        time.sleep(300)

def start_scheduler():
    threading.Thread(target=schedule_cache_updates, daemon=True).start()

def get_random_meme(subreddit_name):
    cached_submissions = r.get(f'subreddit:{subreddit_name}')
    if cached_submissions:
        submissions = json.loads(cached_submissions)
    else:
        subreddit = reddit.subreddit(subreddit_name)  # Fetch subreddit
        submissions = [{
            'title': submission.title,
            'url': submission.url,
            'permalink': submission.permalink
        } for submission in subreddit.hot(limit=690)]  # Fetch memes
        r.setex(f'subreddit:{subreddit_name}', 300, json.dumps(submissions))  # Cache for 5 minutes

    submission = random.choice(submissions)  # Choose random meme
    return submission

@app.route('/')
def home():
    category = request.args.get('category', 'dankmemes')
    meme = get_random_meme(category)
    return render_template('index.html', meme=meme, countdown=30, category=category)

@app.route('/new_meme')
def new_meme():
    category = request.args.get('category', 'dankemems')
    meme = get_random_meme(category)
    return render_template('meme_partial.html', meme=meme, countdown=30)

def main():
    start_scheduler()
    app.run(debug=True)
