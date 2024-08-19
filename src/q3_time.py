import re
import ujson as json
from typing import List, Tuple
from collections import Counter

def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from the given text using a regular expression.
    
    :param text: The input text from which to extract mentions.
    :return: A list of mentions found in the text.
    """
    # Regular expression to find all @mentions
    mention_pattern = re.compile(r"@(\w+)")
    return mention_pattern.findall(text)

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyze tweet data to find the top 10 most mentioned usernames.
    
    :param file_path: Path to the JSON lines file containing tweet data.
    :return: A list of tuples, each containing a username and its mention count.
    """
    mention_counter = Counter()  # Counter to store mention counts

    try:
        # Open the file and process it line by line for better memory efficiency
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    try:
                        tweet = json.loads(line)
                        content = tweet.get('content', '')

                        if content:  # Only process if content is not empty
                            mentions = extract_mentions(content)  # Extract mentions from content
                            mention_counter.update(mentions)  # Update mention counts

                    except json.JSONDecodeError as e:
                        # Handle JSON decode errors gracefully
                        print(f"Skipping line due to JSON decode error: {e}")
                    except KeyError as e:
                        # Handle missing keys in the JSON structure
                        print(f"Skipping line due to missing key: {e}")
                    except Exception as e:
                        # Handle any other unexpected errors
                        print(f"An unexpected error occurred: {e}")

        # Get the top 10 most mentioned usernames
        top_10_mentions = mention_counter.most_common(10)
        return top_10_mentions

    except FileNotFoundError:
        # Handle file not found error
        print(f"Error: File not found - {file_path}")
    except IOError as e:
        # Handle other I/O errors
        print(f"Error reading file {file_path}: {e}")
    except Exception as ex:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {ex}")
    
    return []