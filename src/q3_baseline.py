import json
from collections import Counter
import re
from typing import List, Tuple

# Helper function to load JSON lines 
def load_json_lines(file_path: str):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return data

# Function to extract mentions from text
def extract_mentions(text: str) -> List[str]:
    # Regular expression to find mentions (e.g., @username)
    mention_pattern = re.compile(r"@(\w+)")
    return mention_pattern.findall(text)

# Function to find top 10 most mentioned usernames
def q3_baseline(file_path: str) -> List[Tuple[str, int]]:
    data = load_json_lines(file_path)  # Load the JSON data
    mentions_counter = Counter()

    for tweet in data:
        content = tweet.get("content", "")
        mentions = extract_mentions(content)
        mentions_counter.update(mentions)

    # Get the top 10 most mentioned usernames
    top_10_mentions = mentions_counter.most_common(10)

    return top_10_mentions
