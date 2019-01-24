from twitter_client import twitterClient
from twitter_analyzer import tweet_analyzer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import datetime
import time

if __name__ == "__main__":
    twitter_client = twitterClient("weatherchannel")
    api = twitter_client.get_twitter_api()
    twitter_analyzer = tweet_analyzer()
    tweets = api.user_timeline(screen_name="weatherchannel")  
    twitter_client.get_image_tweet()  
    #Set Start Date and End Date
    """
    start_date = datetime.datetime(2018,9,7)
    end_date = datetime.datetime(2018,9,14)
    tweets_during_florence = twitter_client.get_tweets_between_date(start_date,end_date)
    time.sleep(1)
    df= twitter_analyzer.tweets_to_dataframe(tweets_during_florence)
    df['sentiment'] = np.array([twitter_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
    df.to_csv("data.csv")
    """
    #get Average Length overall 
    #print(np.max(df['likes']))
    #print(df.head(10))
    # Time Series
    #time_retweet = pd.Series(data=df['retweet'].values, index=df['date'])
    #time_retweet.plot(figsize=(16, 4),label="retweets", legend=True)
    #time_retweet = pd.Series(data=df['likes'].values, index=df['date'])
    #time_retweet.plot(figsize=(16, 4),label="likes", legend=True)
    #plt.show()
    time.sleep(1)
