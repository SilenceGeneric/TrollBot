# TrollBot

**TrollBot** is a Python-based tool designed to detect suspicious activities on social media or other platforms. It analyzes posting patterns, identifies repeated phrases, performs sentiment analysis, and detects suspicious account clusters. The program automatically checks for required dependencies and installs them if they are missing.

## Features
- **Abnormal Posting Detection**: Detects accounts with unusual posting frequencies or intervals.
- **Repeated Phrase Detection**: Identifies repeated phrases across posts that exceed a specified threshold.
- **Sentiment Analysis**: Analyzes the sentiment of posts to determine the overall tone.
- **Network Analysis**: Detects suspicious account clusters using graph theory and the `networkx` library.
- **Automatic Dependency Installation**: Automatically checks for required libraries (`networkx`, `textblob`, `python-dateutil`) and installs them if missing.

## How It Works
- **Automatic Dependency Check**: The script will check if the required libraries are already installed. If any are missing, it will automatically install them using `pip`.
- **Abnormal Posting Detection**: Analyzes timestamps of posts for a given account and detects abnormal posting behaviors (e.g., posting too frequently).
- **Repeated Phrase Detection**: Scans posts for repetitive phrases and flags those exceeding the repetition threshold.
- **Sentiment Analysis**: Uses `TextBlob` to analyze the sentiment of posts and calculates an average polarity score.
- **Network Analysis**: Uses `networkx` to identify suspicious clusters of accounts based on mutual connections.

## Functions

### 1. `install_dependencies()`
Checks for missing dependencies and installs them automatically if not found.

### 2. `detect_abnormal_posting(accounts_data, interval_threshold=30, outlier_threshold_stddev=2)`
Detects accounts with abnormal posting patterns by calculating the interval between their posts. Accounts with intervals that are too short or contain outliers are flagged as suspicious.

#### Parameters:
- `accounts_data`: A dictionary where keys are account names, and values are lists of timestamps of their posts.
- `interval_threshold`: Minimum average interval between posts to avoid flagging (in seconds).
- `outlier_threshold_stddev`: Number of standard deviations below the average interval to detect outliers.

#### Returns:
- A list of suspicious accounts.

### 3. `detect_repeated_phrases(posts, repetition_threshold=5, cleaning_regex=r'[^a-zA-Z0-9\s]')`
Detects repeated phrases in a list of posts.

#### Parameters:
- `posts`: A list of post strings.
- `repetition_threshold`: The minimum number of occurrences of a phrase to be considered suspicious.
- `cleaning_regex`: A regex pattern to clean up posts (removes non-alphanumeric characters).

#### Returns:
- A list of repeated phrases that exceed the repetition threshold.

### 4. `sentiment_analysis(posts)`
Analyzes the sentiment of posts and returns the average sentiment polarity.

#### Parameters:
- `posts`: A list of post strings.

#### Returns:
- The average sentiment polarity (a float).

### 5. `analyze_network(accounts, cluster_threshold=20)`
Analyzes the network of accounts and detects suspicious clusters of accounts using graph theory.

#### Parameters:
- `accounts`: A dictionary where keys are account names and values are lists of friends or connections.
- `cluster_threshold`: The minimum size of a suspicious cluster.

#### Returns:
- A list of suspicious clusters.

## Example Usage

```python
sample_accounts = {
    "bot1": ["2025-03-09 12:00:01", "2025-03-09 12:00:05", "2025-03-09 12:00:09"],
    "bot2": ["2025-03-09 11:59:50", "2025-03-09 11:59:55"],
    "human": ["2025-03-09 10:00:00", "2025-03-09 12:30:00"]
}

suspicious = detect_abnormal_posting(sample_accounts)
print("Suspicious accounts:", suspicious)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 
