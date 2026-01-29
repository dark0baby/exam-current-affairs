import requests
import json
from datetime import date

TODAY = date.today().isoformat()
DATA_DIR = f"data/{TODAY}"
MD_FILE = f"{DATA_DIR}/daily_brief.md"
JSON_FILE = "index.json"

# -------- SOURCES (SAFE & EXAM-RELEVANT) --------
SOURCES = {
    "PIB": "https://pib.gov.in/PressReleaseRSS.aspx",
    "RBI": "https://www.rbi.org.in/Scripts/Rss.aspx",
}

def fetch_pib():
    import feedparser
    feed = feedparser.parse(SOURCES["PIB"])
    items = []
    for e in feed.entries[:5]:
        items.append({
            "topic": e.title,
            "why": "Official PIB release",
            "source": "PIB",
        })
    return items

def filter_exam_relevant(items):
    KEYWORDS = [
        "Scheme", "Index", "Report", "Exercise",
        "Launch", "Act", "Bill", "Award", "Appointment"
    ]
    filtered = []
    for i in items:
        if any(k.lower() in i["topic"].lower() for k in KEYWORDS):
            filtered.append(i)
    return filtered

def generate_mcq(topic):
    return {
        "question": f"{topic} is related to which of the following?",
        "options": ["Economy", "Polity", "Science", "Defence"],
        "answer": "Economy"
    }

def main():
    import os
    os.makedirs(DATA_DIR, exist_ok=True)

    raw = fetch_pib()
    filtered = filter_exam_relevant(raw)

    md = f"# Daily Current Affairs – {TODAY}\n\n"
    json_out = []

    for item in filtered:
        mcq = generate_mcq(item["topic"])

        md += f"""## {item['topic']}
**Subject:** Current Affairs  
**Why in News:** {item['why']}  
**Source:** {item['source']}  
**SSC Probability:** HIGH  

**MCQ:**  
Q. {mcq['question']}  
A. {mcq['options']}  
Ans: {mcq['answer']}

---
"""
        json_out.append({
            "date": TODAY,
            "topic": item["topic"],
            "mcq": mcq
        })

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_out, f, indent=2)

if __name__ == "__main__":
    main()
