import json
from datetime import datetime, date
from collections import defaultdict, Counter
from typing import List, Tuple


def load_json_lines(file_path: str):
    """
    Load JSON data from a file where each line is a separate JSON object.

    This function reads a file line by line, parsing each line as a JSON object.

    :param file_path: Path to the JSON lines file
    :return: List of parsed JSON objects
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return data


def q1_baseline(file_path: str) -> List[Tuple[date, str]]:
    """
    Analyze tweet data to find the top 10 dates with the most tweets and the
    most active user for each of these dates.

    This function performs the following steps:
    1. Load the tweet data from the specified file
    2. Count the number of tweets for each date
    3. Count the number of tweets for each user on each date
    4. Identify the top 10 dates with the most tweets
    5. Find the most active user for each of these top 10 dates

    :param file_path: Path to the JSON lines file containing tweet data
    :return: List of tuples, each containing a date and the username of the most active user on that date
    """
    # Load the tweet data
    data = load_json_lines(file_path)

    # Initialize defaultdicts to store the counts
    date_tweet_count = defaultdict(int)
    user_tweet_count_by_date = defaultdict(lambda: defaultdict(int))

    # Process each tweet
    for tweet in data:
        # Extract the date and username from the tweet
        tweet_date = datetime.fromisoformat(tweet["date"]).date()
        username = tweet["user"]["username"]

        # Increment the tweet count for this date
        date_tweet_count[tweet_date] += 1

        # Increment the tweet count for this user on this date
        user_tweet_count_by_date[tweet_date][username] += 1

    # Find the top 10 dates with the most tweets
    top_10_dates = sorted(date_tweet_count.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]

    result = []
    for tweet_date, _ in top_10_dates:
        # Find the user with the most tweets on this date
        top_user = max(
            user_tweet_count_by_date[tweet_date].items(), key=lambda x: x[1]
        )[0]
        result.append((tweet_date, top_user))

    return result
