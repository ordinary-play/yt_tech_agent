import os
import requests
from dotenv import load_dotenv
import praw
from googleapiclient.discovery import build

load_dotenv()

# --- Load keys ---
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

TECH_KEYWORDS = [
    "AI", "ChatGPT", "OpenAI", "Android", "iPhone", "Apple", "Google",
    "Microsoft", "Windows", "Linux", "Python", "JavaScript", "GPT",
    "machine learning", "deep learning", "NVIDIA", "Tesla", "Meta",
    "Samsung", "Technology", "Coding", "Laptop", "Mobile"
]

# --- NewsAPI ---
def fetch_newsapi(page_size=10):
    if not NEWS_API_KEY:
        return []
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    return [a["title"] for a in data.get("articles", []) if "title" in a]

# --- Reddit ---
def fetch_reddit(subreddit="technology", limit=10):
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
        return []
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    return [post.title for post in reddit.subreddit(subreddit).hot(limit=limit)]

# --- YouTube ---
def fetch_youtube_trending(max_results=10, region="IN"):
    if not YOUTUBE_API_KEY:
        return []
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=region,
        videoCategoryId="28",  # Science & Technology
        maxResults=max_results,
    )
    response = request.execute()
    return [item["snippet"]["title"] for item in response.get("items", [])]

# --- Filter tech topics ---
def filter_tech(topics):
    tech = []
    for t in topics:
        if not t:
            continue
        tl = t.lower()
        if any(k.lower() in tl for k in TECH_KEYWORDS):
            tech.append(t)
    return list(set(tech)) or topics

# --- Combine sources ---
def fetch_all_trends():
    topics = []
    topics.extend(fetch_newsapi())
    topics.extend(fetch_reddit())
    topics.extend(fetch_youtube_trending())
    return filter_tech(topics)

if __name__ == "__main__":
    print("Fetching trending tech topics...")
    all_topics = fetch_all_trends()
    for i, t in enumerate(all_topics, 1):
        print(f"{i}. {t}")
