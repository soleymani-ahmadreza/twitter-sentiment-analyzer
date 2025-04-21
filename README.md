# Twitter Sentiment Analyzer
A simple app built using Streamlit, Tweepy, Hugging Face's transformers, and matplotlib. This tool fetches recent tweets based on a user-specified search query, performs sentiment analysis on them, and visualizes the results.

## Features
- Fetch recent tweets based on a query
- Analyze the sentiment of tweets (positive, neutral, negative)
- Visualize sentiment distribution as a pie chart
- Display a word cloud of the most frequent words in tweets
- Export results as a CSV file

## Requirements
To run this project locally, you need to set up the environment with your own Twitter API credentials.

1. Clone this repository:
bash
git clone https://github.com/soleymani-ahmadreza/twitter-sentiment-analyzer.git

2. Install dependencies:
Make sure you have Python installed. Then, install the required Python packages:
bash
pip install -r requirements.txt

3. Set up environment variables:
Create a .env file in the root of the project and add your Twitter API credentials.
bash
TWITTER_BEARER_TOKEN=your_bearer_token_here
You can get your Twitter API Bearer Token by creating a project on the Twitter Developer portal.

4. Run the app:
Once the environment is set up, you can run the Streamlit app:
bash
streamlit run app.py

5. Export results:
You can download the sentiment analysis results as a CSV file from the app.

License
This project is licensed under the MIT License - see the LICENSE file for details.
