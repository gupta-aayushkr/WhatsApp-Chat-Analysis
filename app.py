import streamlit as st
import pandas as pd
import re
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(
    page_icon="💬",
    page_title="WhatsApp Chat Analyzer",
    layout="wide")

#For Reboot
#-----------------------SECTION 1: DATA PREPROCESSING--------------------------------#

def load_data(f):
    #data from text file
    data = f
    # st.write(data)
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
# st.sidebar.selectbox("Select a File")
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# st.write(uploaded_file)

file1 = st.sidebar.file_uploader("Choose a file")

txt_files = []

if file1 is None:
        txt_folder_path = "TXT"
        txt_files = []
        for file in os.listdir(txt_folder_path):
                if file.endswith(".txt"):
                        txt_files.append(file)
        file1 = st.sidebar.selectbox("Select a txt file", txt_files)
        file1 = os.path.join(txt_folder_path, file1)
        # st.write(file1)
        f = open(file1)
        data = f.read()
        f.close()
        # data = pd.read_txt(os.path.join(txt_folder_path, selected_txt))
else:
        f = open(file1)
        data = f.read()
        f.close()

if file1 is not None:
    # bytes_data = file1.getvalue()
    # data = bytes_data.decode("utf-8")
    df = load_data(data)
    # st.write(df)
    # st.write(df)

    #Users
    users_list = df["user"].value_counts()[df["user"].value_counts()>10].reset_index()['user'].tolist()
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
        c1,c2 = st.columns(2)
        nested_c1_left, nested_c1_right = c1.columns(2)

        #Metrics
        nested_c1_left.metric("Total Messages", num_messages)
        nested_c1_left.metric("Total Words", num_words)
        nested_c1_right.metric("Media Shared", num_media)
        nested_c1_right.metric("Time Spent(Days)",round((num_words/(60*24)),2))
    
        #Dataframe
        c2.write("10 Starting WhatsApp Messages (Not shown all for privacy)")
        c2.dataframe(df.head(10), height=300)

    # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Active Users in Group')
            active_users_by_msg = df["user"].value_counts()[df["user"].value_counts()>10].reset_index().head(10)
            overall_active_user_percent_df = round(df["user"].value_counts()[df["user"].value_counts()>10]/df.shape[0]*100).reset_index().rename(columns={'user':'Name', 'count':'Percent'})
            col1, col2 = st.columns(2)

            with col1:
                plt.figure(figsize=(10, 4))
                plt.bar(active_users_by_msg["user"],active_users_by_msg["count"])
                plt.xlabel("UserName")
                plt.ylabel("Message Counts")
                plt.title("User w.r.t. Message Counts")
                plt.xticks(rotation='vertical')
                st.pyplot(plt)
            with col2:
                st.header("Most Messaged (Percent)")
                st.dataframe(overall_active_user_percent_df, width=1000)
        
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

# Preferred Media Type
        st.header("Preferred Media Type")
        media_msg = df[df["message"].str.contains('omitted')]["message"].to_list()
        media_type = []
        for i in media_msg:
            new = re.sub('^a-zA-Z','', i)
            new = new.split()[0]
            media_type.append(new)
        top_media_df =  pd.DataFrame(media_type,columns=['Media']).value_counts().reset_index().head(5)
        c1,c2 = st.columns(2)
        with c1:
            fig = px.pie(top_media_df, names='Media', values='count', title='Media Type Distribution')
            st.plotly_chart(fig)
        with c2:
            st.subheader("Most Sent Media Types")
            st.dataframe(top_media_df, width=500, height=300)



# Timeline analysis
        st.title("Month & Day Activity")
        col1, col2 = st.columns(2)
        #month wise 
        with col1:
            st.write("Monthly Activity")
            plt.clf()
            df['month_num'] = df["date"].dt.month
            timeline_df = df.groupby(['year','month_num', 'month']).count()["message"].reset_index()[1:]
            time = []
            for i in range(1, timeline_df.shape[0]+1):
                time.append(timeline_df["month"][i] + '-' + str(timeline_df["year"][i]))
            timeline_df['time'] = time
            plt.bar(timeline_df['time'], timeline_df['message'], facecolor='green', alpha=0.6)
            plt.scatter(timeline_df['time'], timeline_df['message'], color='blue', marker='o')
            plt.plot(timeline_df['time'], timeline_df['message'], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(plt)

        #daily wise
        with col2:
            st.write("Daily Activity")
            plt.clf()
            df['only_date'] = df['date'].dt.date
            daily_timeline_df = df.groupby('only_date').count()["message"].reset_index()[1:]
            plt.scatter(daily_timeline_df['only_date'], daily_timeline_df['message'], color='red', marker='o', s=1)
            plt.plot(daily_timeline_df['only_date'], daily_timeline_df['message'], color='red', alpha=0.2)
            plt.xticks(rotation='vertical')
            st.pyplot(plt)

        st.title("Weekday & Hourly Activity")
        col1, col2 = st.columns(2)
        #weekday wise
        with col1:
            st.write("Weekday Activity")
            plt.clf()
            df['Weekday'] = df["date"].dt.day_name()
            week_timeline_df = df['Weekday'].value_counts().reset_index()
            plt.bar(week_timeline_df["Weekday"], week_timeline_df["count"], facecolor='green', alpha=0.6)
            plt.scatter(week_timeline_df["Weekday"], week_timeline_df["count"], color='blue', marker='o')
            plt.plot(week_timeline_df["Weekday"], week_timeline_df["count"], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(plt)


        #hour wise
        with col2:
            st.write("Hourly Activity")
            plt.clf()
            period = []
            for hour in df[['hour','Weekday']]['hour']:
                if hour == 23:
                    period. append(str(hour) + "-" + str('00' ))
                elif hour == 0:
                    period.append(str('00') + "-" + str(hour+1))
                else:
                    period.append(str(hour) + "-" + str(hour+1))
            df['period']=period
            hour_timeline_df = df.groupby(['hour','period']).count()["message"].reset_index()
            plt.bar(hour_timeline_df["hour"], hour_timeline_df["message"], facecolor='green', alpha=0.6)
            plt.scatter(hour_timeline_df["hour"], hour_timeline_df["message"], color='blue', marker='o')
            plt.plot(hour_timeline_df["hour"], hour_timeline_df["message"], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(plt)

        if selected_user != 'Overall':
            st.title("Conclusion:")
            user_most_active_weekday = df.groupby('Weekday').count()["message"].sort_values(ascending=False).reset_index()["Weekday"][1]
            user_most_active_hour = df.groupby('hour').count()["message"].sort_values(ascending=False).reset_index()["hour"][1]
            st.info(f"{selected_user} is mostly active on {user_most_active_weekday}. And Mostly prefers to message at {user_most_active_hour}. There top media sent on the chat is {top_media_df['Media'][0]}.")