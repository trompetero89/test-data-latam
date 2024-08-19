from typing import List, Tuple
import datetime
import ujson as json
import re
from heapq import heappush, heappushpop
from collections import defaultdict


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    This function processes a JSON file containing tweet data and determines the top 10 dates with the most tweets.
    For each of these dates, it identifies the user with the most tweets.

    Parameters:
    file_path (str): The path to the JSON file containing tweet data.

    Returns:
    List[Tuple[datetime.date, str]]: A list of tuples where each tuple contains:
        - The date (datetime.date) with a significant number of tweets.
        - The username (str) with the most tweets on that date.
    """

    # Regular expression to extract the date part from the timestamp
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})T")

    # Dictionary to track the tweet count for each user on each date
    date_user_count = defaultdict(lambda: defaultdict(int))

    # Dictionary to track the total number of tweets for each date
    date_total_tweets = defaultdict(int)

    # Min-heap to keep track of the top 10 dates with the most tweets
    top_10_heap = []

    try:
        # Open the JSON file for reading
        with open(file_path, "r", encoding="utf-8") as file:
            # Process each line (tweet) in the file
            for line in file:
                if line.strip():  # Skip empty lines
                    try:
                        # Parse the JSON line into a dictionary
                        tweet = json.loads(line)

                        # Extract the date from the tweet's timestamp
                        date_match = date_pattern.match(tweet["date"])
                        username = tweet["user"]["username"]

                        if date_match and username:
                            date = date_match.group(
                                1
                            )  # Extract the date string (YYYY-MM-DD)
                            user_count = date_user_count[date]

                            # Increment the tweet count for this user on the given date
                            user_count[username] += 1
                            date_total_tweets[date] += 1
                            total_tweets = date_total_tweets[date]

                            # Maintain the top 10 dates with the most tweets using a heap
                            if len(top_10_heap) < 10:
                                heappush(top_10_heap, (total_tweets, date))
                            elif total_tweets > top_10_heap[0][0]:
                                heappushpop(top_10_heap, (total_tweets, date))
                    except (KeyError, AttributeError):
                        # If a tweet is malformed or lacks the necessary data, skip it
                        continue
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return []

    if not top_10_heap:
        print("No valid tweet data found.")
        return []

    # Sort the heap to find the top 10 dates and their respective top users
    result = []
    for _, date in sorted(top_10_heap, reverse=True):
        user_counts = date_user_count[date]

        # Find the user with the most tweets on this date
        top_user = max(user_counts, key=user_counts.get)
        result.append((datetime.date.fromisoformat(date), top_user))

    return result
