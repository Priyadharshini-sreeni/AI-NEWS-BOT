import feedparser
import requests
import os
from deep_translator import GoogleTranslator

# ---------------- CONFIG ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RSS_URL = "https://www.svt.se/nyheter/lokalt/vast/rss.xml"

# ---------------- FETCH + TRANSLATE ----------------
def get_gothenburg_news():
    feed = feedparser.parse(RSS_URL)
    
    message = "📢 <b>Good Morning, Priyadharshini!</b>\n"
    message += "<b>Here are today's Gothenburg news:</b>\n\n"

    for i, entry in enumerate(feed.entries[:10]):
        title_sv = getattr(entry, 'title', 'No title')
        link = getattr(entry, 'link', '')

        # Translate Swedish → English
        title_en = GoogleTranslator(source='sv', target='en').translate(title_sv)

        # Escape HTML
        title_en = title_en.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

        message += f"{i+1}. <a href='{link}'>{title_en}</a>\n\n"

    return message

# ---------------- SEND ----------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print(response.status_code, response.text)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("BOT_TOKEN and CHAT_ID environment variables must be set!")
    news = get_gothenburg_news()
    send_telegram(news)
