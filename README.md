# Reddit Meme Viewer with Flask
This Flask application fetches random memes from Reddit's r/memes subreddit and displays them with a dynamic countdown and a flipping counter for memes viewed.

## Features

- Fetches random memes from Reddit using the Reddit API.
- Displays each meme with its title and a link to the original Reddit post.
- Dynamically updates a countdown for displaying a new meme every 30 seconds.

## Technologies Used

- Python
- Flask
- PRAW (Python Reddit API Wrapper)
- HTML/CSS

## Prerequisites

- Python 3.11 installed
- GitHub account (optional, for deployment)
- Flask

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   
   - Create a `.env` file in the root directory.
   - Add your Reddit API credentials in the `.env` file:
     ```
     CLIENT_ID=your_reddit_client_id
     CLIENT_SECRET=your_reddit_client_secret
     USER_AGENT=your_user_agent
     ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open your web browser and go to `http://localhost:5000` to view the application.

## Usage

- Upon visiting `http://localhost:5000`, the application will fetch and display a random meme from Reddit.
- The meme will be automatically refreshed every 30 seconds.
- Each time a new meme is displayed, the flipping counter for memes viewed increments by 1.

## Deployment

Will deploy soon

## Acknowledgements

- Reddit API for providing access to memes from r/memes.
---