from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def get_meme():
    url = "https://meme-api.herokuapp.com/gimme"
    response = json.loads(requests.get(url).text)
    meme_large = response['preview'][-2]
    subreddit = response['subreddit']
    return meme_large, subreddit

@app.route("/")
def index():
    meme_large, subreddit = get_meme()
    return render_template("index.html", meme_pic=meme_large, subreddit=subreddit)


