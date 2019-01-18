from tweepy import api
from tweepy import cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import twitterkeys

class twitterAuthenticator():
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
                auth = OAuthHandler(twitterkeys.CONSUMER_KEY, twitterkeys.CONSUMER_SECRET)
                auth.set_access_token(twitterkeys.ACCESS_TOKEN, twitterkeys.ACCESS_TOKEN_SECRET)
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
                print(status)

if __name__ == "__main__":
        hashtag_list = ["Florence", "Huricane"]
        fetched_tweets_filename = "tweets.json"
        twitter_streamer = TwitterStreamer()
        twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)


  
