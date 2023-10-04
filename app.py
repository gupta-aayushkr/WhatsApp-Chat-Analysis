import streamlit as st
import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')
import plotly.express as px

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


    #After selecting displaying some basic stats
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

    # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            active_users_by_msg = df["user"].value_counts()[df["user"].value_counts()>10].reset_index().head(10)
            overall_active_user_percent_df = round(df["user"].value_counts()[df["user"].value_counts()>10]/df.shape[0]*100).reset_index().rename(columns={'user':'Name', 'count':'Percent'})
            col1, col2 = st.columns(2)

            with col1:
                plt.bar(active_users_by_msg["user"],active_users_by_msg["count"])
                plt.xlabel("UserName")
                plt.ylabel("Message Counts")
                plt.title("User w.r.t. Message Counts")
                plt.xticks(rotation='vertical')
                st.pyplot(plt)
            with col2:
                st.dataframe(overall_active_user_percent_df, width=1000, height=300)
        
    #worldcloud for each user
        st.header("WordCloud")
        col1,col2 = st.columns(2)

        message_data = df['message'].str.cat(sep=' ')
        message_data = message_data.lower()
        message_data = re.sub('[^a-zA-Z]', ' ', message_data)
        message_data = re.sub('\s+',' ', message_data)

        #importing the stopwords
        stopwords_file = open('stopwords.txt')
        stopwords = stopwords_file.read()
        stopwords_file.close()
        all_stopwords = stopwords.split() + ['haa','kr', 'omitted', 'sticker', 'image', 'https', 'www']

        # filtered message data after removing stopwordss
        filtered_text_data = []
        for word in message_data.split():
            if word.lower() not in all_stopwords:
                filtered_text_data.append(word)
        filtered_text_data = " ".join(filtered_text_data)

        # To view in filtered DF
        filtered_text_df = pd.DataFrame(filtered_text_data.split(), columns=["Words"])
        filtered_text_df = filtered_text_df.value_counts().reset_index()
        filtered_text_df["Freq. %"] = round((filtered_text_df["count"]/filtered_text_df["count"].sum())*100,2)

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text_data)

        with col1:
            st.write("Word Frequencies in Message")
            st.dataframe(filtered_text_df, width=1000)

        with col2:
            plt.clf()
            st.subheader("WordCloud")
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

# not removing stopwords check

