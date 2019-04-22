import json
from typing import *
from basic_sentiment import *

def gatherTweets(file_name: str) -> List:
    '''
    Moves tweets into List
    '''
    tweets = []
    with open("C:/Users/Liam/Documents/EPQ/json_data/data/" + file_name + '.json') as file:
        counter = 0
        for line in file:  #Accounts for .JSON File spacing
            if counter % 2 != 0:
                counter += 1
                continue
            tweets.append(json.loads(line))  #Adds entire tweet information to list
            counter += 1
    return tweets


def abstractTweets(tweets: List) -> Dict:
    '''
    Adds to dictionary based on [date : text]
    '''
    abstracted_tweets = {}
    for tweet in tweets:
        if eliminateSpam(tweet) == True:
            continue
        if tweet["created_at"] in abstracted_tweets: #Accounts for duplicates
            attempt = tweet["created_at"] + '&' #Places symbols to prevent collisions
            while attempt in abstracted_tweets:
                attempt += '&'
            try:
                abstracted_tweets[attempt] = tweet["extended_tweet"]["full_text"]
            except KeyError:
                abstracted_tweets[attempt] = tweet["text"]
        else:
            try:
                abstracted_tweets[tweet["created_at"]] = tweet["extended_tweet"]["full_text"]
            except KeyError:
                abstracted_tweets[tweet["created_at"]] = tweet["text"]
    return abstracted_tweets


def eliminateSpam(tweet : str) -> bool:
    '''
    Eliminate Irrelevant Tweets
    '''
    disallowed_accounts = []
    disallowed_terms = ['RT', 'stream', 'mobile', 'LIVE', 'Live', 'STREAM', 'HD', 'WATCH', 'watch']
    if tweet["lang"] != "en":   #Only accepts English
        return True
    if tweet["user"]["screen_name"] in disallowed_accounts:     #Removes if in dissallowed accounts
        return True
    for term in disallowed_terms:   #Removes if in dissallowed terms
        if term in tweet["text"]:
            return True
    return False
