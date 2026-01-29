import feedparser, os, json
from datetime import date, datetime

# ===============================
# EXAM-FOCUSED SOURCES
# ===============================
PIB_FEEDS = [
    "https://pib.gov.in/rss.xml",
    "https://prsindia.org/rss.xml",
    "https://www.rbi.org.in/Scripts/Rss.aspx"
]

NEWS_FEEDS = [
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://indianexpress.com/section/explained/feed/"
]

# ===============================
# STRICT EXAM TRIGGERS
# ===============================
EXAM_TRIGGERS = [
    "approved", "launched", "scheme", "policy", "bill", "act",
    "index", "ranking", "report", "survey",
    "appointed", "chairman", "governor",
    "summit", "exercise", "mou", "agreement"
]

# ===============================
# DATE & PATHS
# ===============================
today = date.today().isoformat()
dt = datetime.today()
year = dt.year
month = dt.strftime("%Y-%m")

path = f"data/{today}"
os.makedirs(path, exist_ok=True)
daily_file = f"{path}/daily_brief.md"

content = f"# Daily Current Affairs – {today}\n"
content += "_UPSC | SSC | Banking | Railways_\n\n"

# ===============================
# FUNCTION: PROCESS FEEDS
# ===============================
def process_feed(feed_url, strict=False):
    items = []
    feed = feedparser.parse(feed_url)
    for e in feed.entries:
        text = (e.title + " " + e.get("summary", "")).lower()
        if strict:
            if not any(k in text for k in EXAM_TRIGGERS):
                continue
        items.append(e.title)
        if len(items) >= 10:
            break
    return items

# ===============================
# PIB SECTION (PRIMARY)
# ===============================
content += "## Government & Polity (PIB / RBI / PRS)\n"
for src in PIB_FEEDS:
    for title in process_feed(src):
        content += f"• {title}\n"

# ===============================
# FILTERED NEWS SECTION
# ===============================
content += "\n## Important Exam-Relevant Developments\n"
for src in NEWS_FEEDS:
    for title in process_feed(src, strict=True):
        content += f"• {title}\n"

# ===============================
# SAVE DAILY FILE
# ===============================
with open(daily_file, "w", encoding="utf-8") as f:
    f.write(content)

# ===============================
# INDEXING (FIXED)
# ===============================
index_file = "index.json"
if os.path.exists(index_file):
    with open(index_file) as f:
        index = json.load(f)
else:
    index = {"daily": [], "weekly": {}, "monthly": {}, "yearly": {}}

if today not in index["daily"]:
    index["daily"].append(today)

week_id = f"{year}-W{dt.isocalendar()[1]:02d}"

index["weekly"].setdefault(week_id, []).append(today)
index["monthly"].setdefault(month, []).append(week_id)
index["yearly"].setdefault(str(year), []).append(month)

with open(index_file, "w") as f:
    json.dump(index, f, indent=2)
