from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
import sys
import twitterkeys

class twitterClient():
    def __init__(self,twitter_user=None):
        self.auth = twitterAuthenticator().authenticate_twitter()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_twitter_api(self):
        return self.twitter_client

    def get_tweets(self, num_tweet):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweet):
            tweets.append(tweet)
        return tweets
    def get_friend_list(self, num_friends):
        friends = []
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friends.append(friend)
        return friends
    def get_home_tweets(self, num_tweet):
        home_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweet):
            home_tweets.append(tweet)
        return home_tweets

class twitterAuthenticator():
    """
    Authenticate Class for Tweepy
    """
    def authenticate_twitter(self):
        auth = OAuthHandler(twitterkeys.CONSUMER_KEY, twitterkeys.CONSUMER_SECRET)
        auth.set_access_token(twitterkeys.ACCESS_TOKEN, twitterkeys.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
        """
        Class For streaming and processing tweets
        """
        def __init__(self):
            self.twitter_authenticator = twitterAuthenticator()

        def stream_tweets(self, filename, hashtag_list):
                #handle twitter authentication
                listener = twitterListener(filename)
                auth = self.twitter_authenticator.authenticate_twitter()
                stream = Stream(auth, listener)
                stream.filter(track=hashtag_list)

class twitterListener(StreamListener):
        """
        Basic listener class that just prints received tweets to stdout 
        """
        def __init__(self, fetched_tweets_filename):
            self.fetched_tweets_filename = fetched_tweets_filename
                
        def on_data(self,data):
            try:
                print(data)
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
                return True 
            except BaseException as e:
                print("error on_data %s" % str(e))
            return True

        def on_error(self, status):
                if status == 420:
                    #return false on_data method in case of rate limit occurs
                    return False
                print(status)

class tweet_analyzer():
    """
    For analyzing and Categorizing content from tweets    
    """
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['length'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

if __name__ == "__main__":
    twitter_client = twitterClient()
    api = twitter_client.get_twitter_api()
    twitter_analyzer = tweet_analyzer()
    tweets = api.user_timeline(screen_name="weatherchannel", count=20)
    df= twitter_analyzer.tweets_to_dataframe(tweets)
    df['sentiment'] = np.array([twitter_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
    #get Average Length overall 
    print(np.max(df['likes']))
    print(df.head(10))
    # Time Series
    time_retweet = pd.Series(data=df['retweet'].values, index=df['date'])
    time_retweet.plot(figsize=(16, 4),label="retweets", legend=True)
    time_retweet = pd.Series(data=df['likes'].values, index=df['date'])
    time_retweet.plot(figsize=(16, 4),label="likes", legend=True)
    plt.show()

  
