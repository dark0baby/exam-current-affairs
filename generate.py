import os
import json
import feedparser
from datetime import date

TODAY = date.today().isoformat()
DATA_DIR = f"data/{TODAY}"
MD_FILE = f"{DATA_DIR}/daily_brief.md"
JSON_FILE = "index.json"

# ---------- FEEDS ----------
SOURCES = {
    "PIB": "https://pib.gov.in/PressReleaseRSS.aspx",
    "RBI": "https://www.rbi.org.in/Scripts/Rss.aspx",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Indian Express": "https://indianexpress.com/section/india/feed/"
}

# ---------- KEYWORDS ----------
KEYWORDS = [
    "scheme","yojana","policy","budget","gdp","inflation","rbi",
    "supreme court","high court","parliament","cabinet","bill",
    "act","notification","amendment","exercise","defence","launch",
    "appointment","award","report","index","survey","ranking",
    "climate","environment","isro","missile","space","startup",
    "disinvestment","export","import","un","imf","world bank",
    "wto","who","cop","paris agreement"
]

# ---------- MCQ ADAPTIVE ----------
def generate_mcq(topic):
    topic_lower = topic.lower()
    if any(x in topic_lower for x in ["rbi","gdp","budget","inflation","economy"]):
        subject = "Economy"
    elif any(x in topic_lower for x in ["supreme court","high court","parliament","act","bill","amendment"]):
        subject = "Polity"
    elif any(x in topic_lower for x in ["isro","space","missile","science","technology"]):
        subject = "Science & Tech"
    elif any(x in topic_lower for x in ["defence","exercise","army","navy","air force","indigenous"]):
        subject = "Defence"
    else:
        subject = "General Current Affairs"

    question = f"{topic} is related to which of the following?"
    options = ["Economy","Polity","Science & Tech","Defence"]
    answer = subject
    return {"question": question, "options": options, "answer": answer, "subject": subject}

# ---------- MAIN ----------
def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    md_content = f"# Daily Current Affairs – {TODAY}\n\n"
    json_out = []

    total_count = 0
    MAX_ITEMS = 20  # ~1 A4 page

    for source_name, url in SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title","")
            summary = entry.get("summary","")
            text = (title + " " + summary).lower()

            if any(k.lower() in text for k in KEYWORDS):
                mcq = generate_mcq(title)
                md_content += f"""## {title}
**Subject:** {mcq['subject']}
**Why in News:** Key update from {source_name}  
**Source:** {source_name}

**MCQ:**  
Q. {mcq['question']}  
A. {mcq['options']}  
Ans: {mcq['answer']}

---
"""
                json_out.append({"date": TODAY, "topic": title, "source": source_name, "mcq": mcq})
                total_count += 1
                if total_count >= MAX_ITEMS:
                    break
        if total_count >= MAX_ITEMS:
            break

    if total_count == 0:
        md_content += "- No exam-relevant current affairs found for today.\n"

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_out, f, indent=2)

if __name__ == "__main__":
    main()
