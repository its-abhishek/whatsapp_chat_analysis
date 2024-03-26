import re
import pandas as pd

def preprocess(data):
    pattern = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\s*[AP]M)\] (.*?)$'

    messages = []
    dates = []

    for match in re.findall(pattern, data, re.MULTILINE):
        messages.append(match[1].strip())
    messages

    for match in re.findall(pattern, data, re.MULTILINE):
        dates.append(match[0].strip())
    dates

    df = pd.DataFrame({'message_date':dates,'user_message':messages})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%y/%m/%d, %I:%M:%S %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]: # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df["date"].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df