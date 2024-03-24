from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

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

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user, df):
    # Read stop words from file
    with open('english-stop-words-large.txt', 'r') as f:
        stop_words = f.read().splitlines()

    # Filter DataFrame based on selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out certain messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '\u200Eimage omitted')]

    words = []
    # Iterate over messages and extract words
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)  # Append individual word, not the list

    # Create DataFrame with most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df