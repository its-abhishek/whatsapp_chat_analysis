from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch total number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media shared
    num_media_messages = df[df['message'] == '\u200Eimage omitted'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    
    with open('hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    # Filter DataFrame based on selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out certain messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '\u200Eimage omitted\n')]

    def remove_stop_wprds(message):
        y = []

        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_wprds)
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):
    # Read stop words from file
    with open('hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    # Filter DataFrame based on selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out certain messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '\u200Eimage omitted\n')]

    words = []
    # Iterate over messages and extract words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)  # Append individual word, not the list

    # Create DataFrame with most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "." + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline