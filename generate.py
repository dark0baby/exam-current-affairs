import feedparser, os
from datetime import date

# ===============================
# TRUSTED EXAM-FOCUSED RSS FEEDS
# ===============================
SOURCES = [
    # INDIA – GOVERNMENT
    "https://pib.gov.in/rss.xml",
    "https://prsindia.org/rss.xml",
    "https://rbi.org.in/Scripts/Rss.aspx",

    # INDIA – NEWS
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://www.thehindu.com/business/feeder/default.rss",
    "https://indianexpress.com/section/india/feed/",
    "https://indianexpress.com/section/explained/feed/",

    # WORLD – OFFICIAL
    "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
    "https://www.who.int/rss-feeds/news-english.xml",
    "https://www.worldbank.org/en/news/all.rss",
    "https://www.imf.org/en/News/RSS",

    # ENVIRONMENT / SCIENCE
    "https://www.unep.org/rss.xml",
    "https://www.isro.gov.in/rss.xml"
]

# =====================================
# ~100 HIGH-VALUE UPSC + SSC KEYWORDS
# =====================================
KEYWORDS = [
    # POLITY
    "constitution","preamble","fundamental rights","fundamental duties",
    "parliament","lok sabha","rajya sabha","supreme court","high court",
    "judiciary","ordinance","amendment","election commission","federalism",

    # GOVERNMENT & SCHEMES
    "scheme","yojana","mission","initiative","ministry","department",
    "cabinet","policy","act","bill","notification","gazette",

    # ECONOMY
    "budget","gdp","inflation","deflation","repo rate","reverse repo",
    "rbi","monetary policy","fiscal deficit","current account",
    "forex","export","import","msme","startup","disinvestment",

    # INTERNATIONAL
    "un","unodc","unesco","who","imf","world bank","wto",
    "g20","brics","quad","asean","summit","bilateral","multilateral",

    # ENVIRONMENT
    "climate change","global warming","carbon","net zero",
    "biodiversity","wildlife","environment","pollution",
    "cop","paris agreement","renewable","solar","wind",

    # SCIENCE & TECH
    "isro","satellite","missile","space","ai","artificial intelligence",
    "quantum","semiconductor","biotechnology","vaccine","genome",

    # DEFENCE & SECURITY
    "defence","exercise","army","navy","air force","missile",
    "indigenous","drdo","border","cyber security",

    # REPORTS & INDICES
    "report","index","ranking","survey","assessment","outlook"
]

# ===============================
# FILE SYSTEM
# ===============================
today = date.today().isoformat()
path = f"data/{today}"
os.makedirs(path, exist_ok=True)

daily_file = f"{path}/daily_brief.md"

content = f"# Daily Current Affairs – {today}\n\n"
content += "_UPSC | SSC | Railways | Other Govt Exams_\n\n"

count = 0
MAX_ITEMS = 20   # keeps it within ~1 A4 page (font 8–10)

# ===============================
# PARSE & FILTER NEWS
# ===============================
for src in SOURCES:
    feed = feedparser.parse(src)
    for e in feed.entries:
        text = (e.title + " " + e.get("summary","")).lower()
        if any(k in text for k in KEYWORDS):
            content += f"- **{e.title}**\n"
            count += 1
        if count >= MAX_ITEMS:
            break
    if count >= MAX_ITEMS:
        break

# ===============================
# SAVE FILE
# ===============================
with open(daily_file, "w", encoding="utf-8") as f:
    f.write(content)
