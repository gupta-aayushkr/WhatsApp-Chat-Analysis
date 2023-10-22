# WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is an interactive and feature-rich tool that helps you gain valuable insights from your WhatsApp chat history. Analyze your conversations, discover patterns, and extract meaningful information about your chats.

## Features

### 1. Load and Analyze Your Chat

- Import your WhatsApp chat history from a text file.
- Automatic parsing of messages and dates.

### 2. User Selection

- Choose a specific user to analyze their chat activity.
- Option to view group-level statistics for an overall perspective.

### 3. Chat Statistics

- Get an overview of the chat with statistics such as:
  - Total messages sent.
  - Total words used.
  - Number of media shared.
  - Time spent chatting (in days).

### 4. Word Cloud Visualization

- Visualize the most frequently used words in the chat with an interactive word cloud.
- Customize the appearance of the word cloud.

### 5. Media Type Analysis

- Identify the preferred media types shared in the chat.
- View distribution and statistics of media types (e.g., images, stickers, links).

### 6. Timeline Analysis

- Explore monthly and daily chat activity with interactive charts.
- Understand when the chat is most active.
- Discover the most active days of the week and preferred chat hours.

### 7. User-Specific Insights

- If analyzing a specific user, receive personalized insights about their activity.
- Find out the user's most active days and chat hours.

## Dependencies

Ensure you have the following Python libraries installed:

- `streamlit`: For building the interactive web app.
- `pandas`: For data handling and analysis.
- `re`: For regular expressions.
- `wordcloud`: For generating word clouds.
- `matplotlib`: For creating data visualizations.
- `plotly`: For interactive charts.

Install the dependencies using the following command:

```bash
pip install streamlit pandas re wordcloud matplotlib plotly
```

## Usage

1. Clone this repository to your local machine.
2. Install the required dependencies as mentioned above.
3. Run the Streamlit app with the provided Python script.

```bash
python chat_analyzer.py
```

4. Upload your WhatsApp chat history as a text file.
5. Select the user or choose "Overall" for group-level analysis.
6. Click the "Show Analysis" button to explore the insights.

## Author

- Aayush Kumar Gupta