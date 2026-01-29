import feedparser, os
from datetime import date

SOURCES = [
    "https://pib.gov.in/rss.xml",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://indianexpress.com/section/india/feed/",
    "https://news.un.org/feed/subscribe/en/news/all/rss.xml"
]

KEYWORDS = [
    "constitution","parliament","supreme court",
    "scheme","ministry","government",
    "budget","gdp","inflation","rbi",
    "report","index","ranking",
    "un","imf","world bank","climate",
    "environment","defence","exercise"
]

today = date.today().isoformat()
path = f"data/{today}"
os.makedirs(path, exist_ok=True)

daily_file = f"{path}/daily_brief.md"

content = f"# Daily Current Affairs – {today}\n\n"

count = 0
for src in SOURCES:
    feed = feedparser.parse(src)
    for e in feed.entries:
        text = (e.title + " " + e.get("summary","")).lower()
        if any(k in text for k in KEYWORDS):
            content += f"- **{e.title}**\n"
            count += 1
        if count >= 15:
            break

with open(daily_file, "w", encoding="utf-8") as f:
    f.write(content)
