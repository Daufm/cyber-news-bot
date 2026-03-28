import feedparser
import requests
import time
import os
import html
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/"
]

POSTED_FILE = "posted.txt"

def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_posted(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=data)
    print("📡 Telegram response:", response.text)  # Show API response

def fetch_news():
    posted = load_posted()
    print("📂 Loaded posted links:", len(posted))

    for feed_url in FEEDS:
        print(f"🌐 Fetching: {feed_url}")
        feed = feedparser.parse(feed_url)
        print("📰 Entries found:", len(feed.entries))

        for entry in feed.entries[:5]:
            print("➡️ Checking:", entry.title)

            if entry.link not in posted:
                print("✅ NEW → sending")

                # Escape HTML to prevent Telegram rejection
                title = html.escape(entry.title)
                summary = html.escape(getattr(entry, "summary", "No summary"))

                message = f"""
<b>{title}</b>

{summary[:200]}...

🔗 {entry.link}

#CyberSecurity #InfoSec
"""
                send_message(message)
                save_posted(entry.link)
                time.sleep(3)  # avoid spamming
            else:
                print("⚠️ Already posted")

def main():
    print("🚀 Bot started...")

    while True:
        print("🔄 Checking for news...")
        fetch_news()
        print("⏳ Sleeping for 1 minute...")
        time.sleep(60)  # 1-minute interval

if __name__ == "__main__":
    main()
