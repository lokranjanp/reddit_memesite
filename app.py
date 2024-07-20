from flask import Flask, render_template
import praw
import random
import os

app = Flask(__name__)   # initialised new flask app

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


@app.route('/')
def home():
    subreddit = reddit.subreddit('dankmemes')   # fetch subreddit
    submissions = list(subreddit.hot(limit=690))    # fetch memes
    submission = random.choice(submissions)     # choose random meme
    meme = {
        'title': submission.title,
        'url': submission.url,
        'permalink': submission.permalink
    }
    return render_template('index.html', meme=meme, countdown=30)


if __name__ == '__main__':
    app.run(debug=True)
