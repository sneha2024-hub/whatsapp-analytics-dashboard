from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

# Initialize URL extractor
extract = URLExtract()

# Load stop words once at the beginning
try:
    with open('pythonProject/stop_hinglish.txt', 'r', encoding="utf-8") as f:
        # Store as lowercase for consistent comparison
        stop_words = [w.strip().lower() for w in f.readlines() if w.strip()]
except FileNotFoundError:
    print("Error: 'stop_hinglish.txt' file not found.")
    stop_words = []  # Default to an empty list if file is missing


def fetch_stats(selected_user, df):
    """
    Returns:
    - num_messages: total messages
    - num_words: total words
    - num_media_messages: media messages count
    - num_links: total URLs
    """
    # Filter by user if specified
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total number of messages
    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['message']:
        words.extend(str(message).split())

    # Handle both '<Media omitted>' and '<Media omitted>\n'
    media_markers = ['<Media omitted>', '<Media omitted>\n']
    num_media_messages = df[df['message'].isin(media_markers)].shape[0]

    # Total number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(str(message)))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    """
    Returns:
    - x: top 5 users by message count (Series)
    - df_percent: dataframe of user-wise percentage contribution
    """
    x = df['user'].value_counts().head()
    df_percent = (
        (df['user'].value_counts() / df.shape[0]) * 100
    ).round(2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df_percent


def create_wordcloud(selected_user, df, exclude_words=None):
    if exclude_words is None:
        exclude_words = []

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    media_markers = ['<Media omitted>', '<Media omitted>\n']
    temp = temp[~temp['message'].isin(media_markers)]

    # Clean exclude_words to lowercase
    exclude_words = [w.lower() for w in exclude_words]

    # Remove stop words and excluded words
    def remove_stop_words(message: str) -> str:
        tokens = str(message).lower().split()
        filtered = [
            word for word in tokens
            if (word not in stop_words) and (word not in exclude_words)
        ]
        return " ".join(filtered)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    temp = temp.copy()
    temp['message'] = temp['message'].apply(remove_stop_words)

    all_text = temp['message'].str.cat(sep=" ")
    if not all_text.strip():
        # In case everything is stop words and we get empty string
        all_text = "whatsapp chat"

    df_wc = wc.generate(all_text)
    return df_wc


def most_common_words(selected_user, df, exclude_words=None):
    if exclude_words is None:
        exclude_words = []

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    media_markers = ['<Media omitted>', '<Media omitted>\n']
    temp = temp[~temp['message'].isin(media_markers)]

    exclude_words = [w.lower() for w in exclude_words]

    words = []

    # Collect non-stop words
    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words and word not in exclude_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    """
    Returns a dataframe of emojis and their counts (sorted).
    Safe even if no emojis exist.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])

    if not emojis:
        return pd.DataFrame(columns=[0, 1])  # empty df with expected columns

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap
