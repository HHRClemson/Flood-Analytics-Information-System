from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

import twitterkeys

class TwitterStreamer():
        """
        Class For streaming and processing tweets
        """
        def stream_tweets(self, filename, hashtag_list):
                #handle twitter authentication
                listener = StdOutListener()
                auth = OAuthHandler(twitterkeys.CONSUMER_KEY, twitterkeys.CONSUMER_SECRET)
                auth.set_access_token(twitterkeys.ACCESS_TOKEN, twitterkeys.ACCESS_TOKEN_SECRET)
                stream = Stream(auth, listener)
                stream.filter(track=hashtag_list)

class StdOutListener(StreamListener):
        """
        Basic listener class that just prints received tweets to stdout 
        """
        def __init__(self, fetched_tweets_filename):
                
        def on_data(self,data):
                print(data)
                return True

        def on_error(self, status):
                print(status)

if __name__ == "__main__":
        


  

