import re
import ujson as json
from typing import List, Tuple
from collections import Counter

# Compile emoji pattern to match various emoji ranges
EMOJI_PATTERN = re.compile(
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
        "\U000024C2-\U0001F251"  # Enclosed Characters
    "]+", 
    flags=re.UNICODE
)

def extract_emojis(text: str) -> List[str]:
    """
    Extract emojis from the given text using the compiled regex pattern.
    
    :param text: The input text from which to extract emojis.
    :return: A list of emojis found in the text.
    """
    return EMOJI_PATTERN.findall(text)

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyze tweet data to find the top 10 most used emojis.
    
    :param file_path: Path to the JSON lines file containing tweet data.
    :return: List of tuples, each containing an emoji and its count.
    """
    emoji_counter = Counter()
    processed_tweets = 0

    try:
        # Open the file and process it line by line
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if not line.strip():  # Skip empty lines
                    continue
                
                try:
                    # Attempt to parse the JSON line
                    tweet = json.loads(line)
                    content = tweet.get('content', '')  # Get the tweet content
                    
                    if content:  # Process only if content is not empty
                        emojis = extract_emojis(content)  # Extract emojis from content
                        emoji_counter.update(emojis)  # Update the emoji counts
                        processed_tweets += 1

                        # Print progress every 100,000 tweets
                        if processed_tweets % 100000 == 0:
                            print(f"Processed {processed_tweets} tweets")
                
                except json.JSONDecodeError:
                    # Silently skip lines with JSON decode errors
                    continue
                except KeyError as e:
                    # Handle missing keys in the tweet JSON
                    print(f"Missing key: {e}, skipping line.")
                    continue

    except FileNotFoundError:
        # Handle file not found error
        print(f"Error: File not found - {file_path}")
        return []
    except IOError as e:
        # Handle any other I/O errors
        print(f"Error reading file {file_path}: {e}")
        return []
    except Exception as ex:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {ex}")
        return []

    # Get the top 10 most used emojis
    top_10_emojis = emoji_counter.most_common(10)
    
    # Output the total number of processed tweets
    print(f"Total processed tweets: {processed_tweets}")
    
    return top_10_emojis