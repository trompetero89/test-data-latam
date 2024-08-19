import json
from collections import Counter
import re
from typing import List, Tuple

# Helper function to load JSON lines (as discussed earlier)
def load_json_lines(file_path: str):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return data

# Function to extract emojis from text
def extract_emojis(text: str) -> List[str]:
    # This regular expression matches most emojis
    emoji_pattern = re.compile(
        "["  
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols, etc.
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.findall(text)

# Function to find top 10 most used emojis
def q2_baseline(file_path: str) -> List[Tuple[str, int]]:
    data = load_json_lines(file_path)  # Load the JSON data
    emoji_counter = Counter()

    for tweet in data:
        content = tweet.get("content", "")
        emojis = extract_emojis(content)
        emoji_counter.update(emojis)

    # Get the top 10 most common emojis
    top_10_emojis = emoji_counter.most_common(10)

    return top_10_emojis