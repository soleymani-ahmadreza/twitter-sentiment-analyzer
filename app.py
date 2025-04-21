
import os
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dotenv import load_dotenv
from transformers import pipeline
import tweepy

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter API client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Load sentiment model
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

sentiment_pipeline = load_sentiment_model()

# Fetch tweets from Twitter API
def search_tweets(query, max_results=20):
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["text", "lang"]
        )
        return [tweet.text for tweet in response.data] if response.data else []
    except tweepy.TooManyRequests as e:
        reset_time = e.response.headers.get("x-rate-limit-reset")
        reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(reset_time)))
        st.error(f"Rate limit exceeded. Try again after {reset_time}.")
        time.sleep(15 * 60)
        return search_tweets(query, max_results)
    except Exception as e:
        st.error(f"Error fetching tweets: {e}")
        return []

# Analyze sentiments
def analyze_sentiment(texts):
    try:
        return sentiment_pipeline(texts)
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        return []

# Pie chart for sentiment distribution
def plot_sentiment_pie_chart(counts):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [counts['POSITIVE'], counts['NEUTRAL'], counts['NEGATIVE']]
    colors = ['#66b3ff', '#99ff99', '#ff6666']
    explode = (0.1, 0, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

# Word cloud visualization
def plot_word_cloud(tweets):
    all_text = " ".join(tweets)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    st.image(wordcloud.to_array(), caption="Most Frequent Words in Tweets", use_column_width=True)

# Streamlit UI
st.title("🧠 Twitter Sentiment Analyzer")
query = st.text_input("🔍 Search tweets about...")

if query:
    with st.spinner("Fetching tweets..."):
        tweets = search_tweets(query)

    if tweets:
        st.success(f"Fetched {len(tweets)} tweets.")
        with st.spinner("Analyzing sentiment..."):
            results = analyze_sentiment(tweets)

        df = pd.DataFrame({
            "Tweet": tweets,
            "Sentiment": [r["label"] for r in results],
            "Score": [r["score"] for r in results],
        })

        st.download_button(
            label="💾 Download results as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="tweet_sentiments.csv",
            mime="text/csv",
        )

        st.subheader("🧾 Sentiment Breakdown")
        sentiment_counts = df["Sentiment"].value_counts().reindex(["POSITIVE", "NEUTRAL", "NEGATIVE"], fill_value=0)
        st.write(f"🙂 Positive: {sentiment_counts['POSITIVE']}")
        st.write(f"😐 Neutral: {sentiment_counts['NEUTRAL']}")
        st.write(f"🙁 Negative: {sentiment_counts['NEGATIVE']}")

        st.subheader("📊 Sentiment Distribution")
        plot_sentiment_pie_chart(sentiment_counts)

        st.subheader("🧑‍💻 Word Cloud of Frequent Words")
        plot_word_cloud(tweets)

        st.subheader("📌 Sample Tweets")
        for tweet, sentiment in zip(tweets, results):
            st.markdown(f"> {tweet}\n\n→ Sentiment: **{sentiment['label']}**")
    else:
        st.warning("No tweets found.")
