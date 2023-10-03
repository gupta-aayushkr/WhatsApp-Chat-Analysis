import streamlit as st
import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

#-----------------------SECTION 1: DATA PREPROCESSING--------------------------------#

def load_data(f):
    #data from text file
    data = f

    #separting message and date
    pattern = "\[\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\s[APap][Mm]\]\s"
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message':message, 'date':dates})
    df['date'] = pd.to_datetime(df['date'],format='[%d/%m/%y, %I:%M:%S %p] ')

    #Separting user and message
    users = []
    messages = []
    for message in df['user_message']:
        line = re.split('([\w\W]+?):\s', message)
        users.append(line[1])
        messages.append(line[2])
    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)
    
    #Extracting Years, Months, Days
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df


#-----------------------SECTION 3: MAIN--------------------------------#

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = load_data(data)
    st.write(df)

    #Users
    users_list = df["user"].unique().tolist()
    if len(users_list) > 2:
        users_list.remove(users_list[0])
    users_list.sort()
    users_list.insert(0, "Overall")        
    selected_user = st.sidebar.selectbox("Select User to Analyze", users_list)

    #Statistics
    if selected_user != 'Overall':
        df = df[df["user"]==selected_user]

    num_messages = len(df["message"])
    words = []
    for word in df["message"]:
        for i in word.split():
            words.append(i)
    
    num_words = len(words)
    num_media = df[df["message"].str.contains(r'omitted',case=False, regex=True)]["message"].value_counts().sum()


        #     with col1:
        #     st.header("Total Messages")
        #     st.title(num_messages)
        # with col2:
        #     st.header("Total Words")
        #     st.title(words)
        # with col3:
        #     st.header("Media Shared")
        #     st.title(num_media_messages)
        # with col4:
        #     st.header("Links Shared")
        #     st.title(num_links)

    #After selecting user performing analysis
    if st.sidebar.button("Show Analysis"):
        st.title("Statistics")
        c1,c2,c3,c4 = st.columns(4)

        #c1
        c1.header("Total Messages")
        c1.title(num_messages)

        #c2
        c2.header("Total Words")
        c2.title(num_words)

        #c3
        c3.header("Media Shared")
        c3.title(num_media)

                #c3
        c4.header("Time Spent(Days)")
        c4.title(round((num_words/(60*24)),2))

