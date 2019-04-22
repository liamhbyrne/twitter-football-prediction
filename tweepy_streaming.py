from tweepy.streaming import StreamListener  #Class that gathers tweets
from tweepy import OAuthHandler, Stream  #Authenticator
import tweepy_creds
from abstract_tweets import eliminateSpam
import json

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def stream_tweets(self, hashtag_teams):
        listener = OverriddenListener(hashtag_teams)  # Instance
        creds = OAuthHandler(tweepy_creds.CONSUMER_KEY, tweepy_creds.CONSUMER_SECRET)  # Consumer keys given to authenticator
        creds.set_access_token(tweepy_creds.ACCESS_TOKEN, tweepy_creds.ACCESS_TOKEN_SECRET)  # access token given
        stream = Stream(creds, listener)  # Start Streaming, (authentication, object)        hashtags = ["#FFC", "#CFC", "#LUFC", "#NUFC"]  # Keywords
        stream.filter(track=[*hashtag_teams])  # Filter based on keywords

class OverriddenListener(StreamListener): #Class inherits the tweet gatherer
    """
    Handles incoming tweets
    """
    def __init__(self, hashtag_teams):
        self.hashtag_teams = hashtag_teams

    def on_data(self, data): #Takes data from listener
        datum = json.loads(data)
        if eliminateSpam(datum) == True:
            return True #Terminates addition
        datum_text = data.lower()
        print(data)
        for i in self.hashtag_teams:
            if i in datum_text:
                print("Written ::= " + data)
                with open("C:/Users/Liam/Documents/EPQ/json_data/data/" + self.hashtag_teams[i], 'a') as file:
                    file.write(data)
        return True  #Stop

    def on_error(self, status): #Print
        #encountered error
        if status == 420: #Catches error
            print("420 - LIMIT REACHED")
            return False
        if status == 401:
            print("UNAUTHORISED")
            return False
        print(status)

hashtag_teams = {'#avfc' : 'avfc2204.json',
                 '#millwall' : 'millwall2204.json'} #keyword s, LOWERCASE, Including hashtags

twitter_streamer = TwitterStreamer()
twitter_streamer.stream_tweets(hashtag_teams)
