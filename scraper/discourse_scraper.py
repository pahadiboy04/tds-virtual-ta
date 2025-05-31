import requests
import json
from datetime import datetime

def scrape_posts(start_date, end_date, output_path="data/discourse.json"):
    base = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json"
    r = requests.get(base)
    topics = r.json()["topic_list"]["topics"]
    results = []

    for topic in topics:
        topic_id = topic["id"]
        created = topic["created_at"][:10]
        if start_date <= created <= end_date:
            topic_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json"
            topic_data = requests.get(topic_url).json()
            for post in topic_data["post_stream"]["posts"]:
                results.append({
                    "topic": topic["title"],
                    "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}/{post['post_number']}",
                    "content": post["cooked"]
                })

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

# Example:
# scrape_posts("2025-01-01", "2025-04-14")
