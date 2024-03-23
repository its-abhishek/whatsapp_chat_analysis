from urlextract import URLExtract
from wordcloud import WordCloud

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