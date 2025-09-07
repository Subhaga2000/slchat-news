import os
import json
import time
import html
import feedparser
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# --- CONFIG ---
FEEDS = [
    "https://www.adaderana.lk/rss.php",
    # add other RSS URLs here, e.g. "https://www.dailynews.lk/rss", etc.
]

SENT_FILE = "data/sent_ids.json"

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
# ---------------

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("ERROR: TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set as environment variables.")
    raise SystemExit(1)

def load_sent():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_sent(sent):
    os.makedirs(os.path.dirname(SENT_FILE), exist_ok=True)
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(sent, f, ensure_ascii=False, indent=2)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    resp = requests.post(url, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()

def summarize(text, max_len=350):
    t = html.unescape(text or "")
    if len(t) > max_len:
        return t[:max_len].rsplit(" ", 1)[0] + "..."
    return t

def make_message(entry):
    title = entry.get("title", "No title")
    link = entry.get("link", "")
    summary = entry.get("summary", entry.get("description", ""))
    summary = summarize(summary, max_len=300)
    # escape HTML
    title_e = html.escape(title)
    summary_e = html.escape(summary)
    link_e = html.escape(link)
    msg = f"<b>{title_e}</b>\n{summary_e}\n\n<a href='{link_e}'>Read more</a>"
    return msg

def main():
    sent = load_sent()
    new_sent = False

    for feed_url in FEEDS:
        d = feedparser.parse(feed_url)
        entries = d.entries or []
        # iterate newest first
        for entry in entries:
            entry_id = entry.get("id") or entry.get("link")
            if not entry_id:
                continue
            if entry_id in sent:
                continue
            try:
                msg = make_message(entry)
                send_telegram(msg)
                print("Sent:", entry.get("title"))
                sent.append(entry_id)
                new_sent = True
                # polite delay
                time.sleep(1)
            except Exception as e:
                print("Failed to send:", entry.get("title"), "->", e)

    if new_sent:
        save_sent(sent)

if __name__ == "__main__":
    main()
