import subprocess
import sys
import os
import logging
import traceback
import re
from collections import defaultdict
from datetime import datetime
import statistics

# Check and install dependencies if missing
def install_dependencies():
    try:
        import networkx as nx
        from textblob import TextBlob
        from dateutil import parser
    except ImportError:
        print("Dependencies not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "networkx", "textblob", "python-dateutil"])
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

# Call to install dependencies before running the program
install_dependencies()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_abnormal_posting(accounts_data, interval_threshold=30, outlier_threshold_stddev=2):
    """Detects accounts with abnormal posting patterns."""
    if not isinstance(accounts_data, dict):
        logging.error("Error: accounts_data must be a dictionary.")
        return []

    suspicious_accounts = []
    for account, timestamps in accounts_data.items():
        if not timestamps:
            continue
        try:
            if not isinstance(timestamps, list):
                raise TypeError(f"Timestamps for account '{account}' must be a list.")
            for ts in timestamps:
                if not isinstance(ts, str):
                    raise TypeError(f"Timestamp '{ts}' for account '{account}' is not a string.")

            parsed_timestamps = []
            for ts in timestamps:
                try:
                    parsed_timestamps.append(parser.parse(ts))
                except ValueError as e:
                    logging.error(f"Error parsing timestamp '{ts}' for account '{account}': {e}. Full timestamps: {timestamps}")
                    continue

            if len(parsed_timestamps) < 2:
                continue

            timestamps = sorted(parsed_timestamps)
            intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]

            if intervals:
                avg_interval = sum(intervals) / len(intervals)
                if avg_interval < interval_threshold:
                    if account not in suspicious_accounts:
                        suspicious_accounts.append(account)

                if len(intervals) > 1:
                    stddev = statistics.stdev(intervals)
                    for interval in intervals:
                        if interval < interval_threshold and interval < (avg_interval - (outlier_threshold_stddev * stddev)):
                            if account not in suspicious_accounts:
                                suspicious_accounts.append(account)

        except (TypeError, Exception) as e:
            logging.error(f"Error processing account '{account}': {e}. Full timestamps: {timestamps}")
            logging.debug(traceback.format_exc())

    return suspicious_accounts

def detect_repeated_phrases(posts, repetition_threshold=5, cleaning_regex=r'[^a-zA-Z0-9\s]'):
    """Detects repeated phrases in a list of posts."""
    if not isinstance(posts, list):
        logging.error("Error: posts must be a list.")
        return []

    phrase_counts = defaultdict(int)
    for post in posts:
        if not isinstance(post, str):
            logging.error(f"Error: Post '{post}' is not a string.")
            continue
        try:
            cleaned_post = re.sub(cleaning_regex, '', post.lower()).strip()
            phrase_counts[cleaned_post] += 1
        except Exception as e:
            logging.error(f"Error processing post '{post}': {e}")
            logging.debug(traceback.format_exc())

    return [phrase for phrase, count in phrase_counts.items() if count > repetition_threshold]

def sentiment_analysis(posts):
    """Performs sentiment analysis on a list of posts."""
    if not isinstance(posts, list):
        logging.error("Error: posts must be a list.")
        return 0

    if not posts:
        logging.info("No posts provided for sentiment analysis.")
        return 0

    sentiments = []
    for post in posts:
        if not isinstance(post, str):
            logging.error(f"Error: Post '{post}' is not a string.")
            continue
        try:
            sentiments.append(TextBlob(post).sentiment.polarity)
        except Exception as e:
            logging.error(f"Error analyzing sentiment of post '{post}': {e}")
            logging.debug(traceback.format_exc())

    if not sentiments:
        logging.info("No valid posts for sentiment analysis.")
        return 0

    return sum(sentiments) / len(sentiments)

def analyze_network(accounts, cluster_threshold=20):
    """Analyzes a network of accounts and detects suspicious clusters."""
    if not isinstance(accounts, dict):
        logging.error("Error: accounts must be a dictionary.")
        return []

    G = nx.Graph()
    for account, friends in accounts.items():
        if not isinstance(friends, list):
            logging.error(f"Error: 'friends' for account '{account}' must be a list.")
            continue
        if not isinstance(account, str):
            logging.error(f"Error: Account key '{account}' must be a string.")
            continue
        for friend in friends:
            if not isinstance(friend, str):
                logging.error(f"Error: Friend '{friend}' for account '{account}' is not a string.")
                continue
            try:
                G.add_edge(account, friend)
            except Exception as e:
                logging.error(f"Error adding edge between '{account}' and '{friend}': {e}")
                logging.debug(traceback.format_exc())

    suspicious_clusters = [list(component) for component in nx.connected_components(G) if len(component) > cluster_threshold]
    return suspicious_clusters

if __name__ == "__main__":
    sample_accounts = {
        "bot1": ["2025-03-09 12:00:01", "2025-03-09 12:00:05", "2025-03-09 12:00:09", "2025/03/09 12:00:13", "2025-03-09 12:05:00"],
        "bot2": ["2025-03-09 11:59:50", "2025-03-09 11:59:55", "2025-03-09 12:00:02"],
        "human": ["2025-03-09 10:00:00", "2025-03-09 12:30:00", "2025-03-09 12:31:00", "2025-03-09 12:32:00", "2025-03-09 12:33:00", "2025-03-09 12:34:00"],
        "empty": []
    }

    try:
        suspicious = detect_abnormal_posting(sample_accounts)
        print("Suspicious accounts:", suspicious)
    except Exception as e:
        logging.error("An error occurred during abnormal posting detection.")
        logging.debug(traceback.format_exc())
