from typing import List, Tuple
import datetime
import json
from heapq import heappush, heappushpop
from collections import defaultdict


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
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

    # Dictionary to store the total number of tweets per date
    date_total_tweets = {}

    # Min-heap to keep track of the top 10 dates with the most tweets
    top_10_heap = []

    # Size of the chunk to process in each iteration (1 million tweets)
    chunk_size = 1000000

    try:
        # Open the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                # Dictionary to store tweet counts per user per date in the current chunk
                chunk = defaultdict(lambda: defaultdict(int))

                # Process a chunk of tweets
                for _ in range(chunk_size):
                    line = file.readline()
                    if not line:  # Break if end of file is reached
                        break

                    try:
                        tweet = json.loads(line)  # Parse the tweet
                        date_str = tweet.get("date")  # Extract the tweet date
                        username = tweet.get("user", {}).get(
                            "username"
                        )  # Extract the username

                        if date_str and username:
                            # Convert the date string to a date object
                            date = datetime.datetime.strptime(
                                date_str, "%Y-%m-%dT%H:%M:%S%z"
                            ).date()
                            # Increment the user's tweet count for the date
                            chunk[date][username] += 1
                    except (json.JSONDecodeError, ValueError):
                        # Ignore malformed lines or invalid data
                        continue

                # Update the top 10 dates with the most tweets and their counts
                for date, user_counts in chunk.items():
                    total_tweets = sum(user_counts.values())
                    date_total_tweets[date] = (
                        date_total_tweets.get(date, 0) + total_tweets
                    )

                    if len(top_10_heap) < 10:
                        # Push the date onto the heap if there are fewer than 10 dates
                        heappush(top_10_heap, (date_total_tweets[date], date))
                    elif date_total_tweets[date] > top_10_heap[0][0]:
                        # Replace the smallest element if the current date has more tweets
                        heappushpop(top_10_heap, (date_total_tweets[date], date))

                # Clear the chunk to free memory before processing the next chunk
                chunk.clear()

                if not line:  # End of file check
                    break

        if not top_10_heap:
            print("No valid data found in the file.")
            return []

        # Find the most active user on each of the top 10 dates
        result = []
        for _, date in sorted(top_10_heap, reverse=True):
            with open(file_path, "r", encoding="utf-8") as file:
                user_counts = defaultdict(int)
                for line in file:
                    try:
                        tweet = json.loads(line)
                        tweet_date = datetime.datetime.strptime(
                            tweet["date"], "%Y-%m-%dT%H:%M:%S%z"
                        ).date()
                        if tweet_date == date:
                            user_counts[tweet["user"]["username"]] += 1
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
                top_user = max(user_counts, key=user_counts.get)
                result.append((date, top_user))

        return result

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []
