import streamlit as st
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")

upload_file = st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique user
    # Check if 'group_notification' exists in the 'user' column
    if 'group_notification' in df['user'].unique():
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
    else:
        # If 'group_notification' doesn't exist, proceed with usual process
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # if st.sidebar.button("Show Analysis"):

    #     num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    #     col1, col2, col3, col4 = st.columns(4)

    #     with col1:
    #         st.header("Total Messages")
    #         st.title(num_messages)
        
    #     with col2:
    #         st.header("Total Words")
    #         st.title(words)

    #     with col3:
    #         st.header("Media Shared")
    #         st.title(num_media_messages)

    #     with col4:
    #         st.header("Links Shared")
    #         st.title(num_links)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        headers = ["Total Messages", "Total Words", "Media Shared", "Links Shared"]
        titles = [num_messages, words, num_media_messages, num_links]

        for header, title in zip(headers, titles):
            with st.columns(4)[headers.index(header)]:
                st.header(header)
                st.title(title)
        
