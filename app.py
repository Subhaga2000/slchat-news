from flask import Flask, render_template, jsonify
import feedparser

app = Flask(__name__)

FEEDS = [
    "https://www.adaderana.lk/rss.php",
]

def get_latest_news(limit=20):
    news_list = []
    for feed_url in FEEDS:
        d = feedparser.parse(feed_url)
        for entry in d.entries[:limit]:
            # Try to get an image from RSS
            img_url = ""
            if 'media_content' in entry:
                img_url = entry.media_content[0]['url']
            elif 'links' in entry:
                for link in entry.links:
                    if link.type.startswith("image/"):
                        img_url = link.href
                        break
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "image": img_url
            })
    return news_list

@app.route("/")
def home():
    news_list = get_latest_news()
    return render_template("index.html", news_list=news_list)

@app.route("/api/news")
def api_news():
    return jsonify(get_latest_news())

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
