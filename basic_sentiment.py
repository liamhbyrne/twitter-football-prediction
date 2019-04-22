from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import *
import re
import matplotlib.pyplot as plt
import datetime
from matplotlib import style
import random
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from wordcloud import WordCloud


def getSentiment(tweets : Dict):
    print("Getting sentiment...")
    analyzer = SentimentIntensityAnalyzer()  #Creates a vaderSentiment object
    for t in tweets:
        averages = []
        sentences = nltk.sent_tokenize(extractText(tweets[t]))
        for i in sentences:
            vs = analyzer.polarity_scores(i)  #Retrieves sentiment scores
            averages.append(vs["compound"])  #adds each sentence polarity to a list so an average can be taken.
        mean = sum(averages) / len(averages)
        tweets[t] = (extractText(tweets[t]), mean)  #Extracts compound score
    return tweets


def extractText(tweet: str)-> str:  #Regular expression to remove hyperlinks and hashtags
    result = re.sub("http\S+", "", tweet)
    result = re.sub("#\S+", "", result)
    result = re.sub("@\S+", "", result)
    return result


def AverageByTime(tweets: Dict)-> Dict:
    print("Finding averages...")
    polarised_time = {}
    initial_time = datetime.datetime.strptime(list(tweets.keys())[0], "%a %b %d %H:%M:%S %z %Y")  #Gets time of first tweet
    time_gap = int(input("Choose a time interval between values:\n>>>"))  #Collects value from user for intervals
    next_time = initial_time + datetime.timedelta(minutes=time_gap)
    current_polarity = []
    for t in tweets:
        time = t
        while '&' in time:
            time = time.replace("&", "")
        time = datetime.datetime.strptime(time, "%a %b %d %H:%M:%S %z %Y")
        if time <= next_time:
            current_polarity.append(float(tweets[t][1]))
            continue
        else:
            total = sum(current_polarity)
            elements = len(current_polarity)
            result = total / elements
            formatted_time = time.strftime("%a %b %d %H:%M:%S %z %Y")
            polarised_time[formatted_time] = result
            initial_time = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %z %Y")
            next_time = initial_time + datetime.timedelta(minutes=time_gap)
            current_polarity = []
    return polarised_time


def findAverage(polarised_tweets: Dict) -> float:
    total: float = 0.0
    total_squared : float = 0.0
    for t in polarised_tweets:
        total += float(polarised_tweets[t][1])
        total_squared += float(polarised_tweets[t][1]**2)
    mean = total / len(polarised_tweets)
    standard_deviation = (total_squared / len(polarised_tweets)) - mean**2
    print("σx̅ : " + str(standard_deviation))
    return mean


def plotGraph(time_polarity: Dict, kick_off_hour : int, kick_off_minute : int, title : str) -> None:
    print("plotting...")
    style.use('Solarize_Light2')  #Sets style and labels
    plt.xlabel('Time, (\m)')
    plt.ylabel('Sentiment Polarity (-1 -> 1)')
    plt.title(title)
    x = []
    y = []
    for t in time_polarity:
        y.append(time_polarity[t])
        minute = datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %z %Y") - datetime.timedelta(hours=kick_off_hour, minutes=kick_off_minute)  #Sets time at minute 0
        minute = minute.strftime("%H:%M:%S")
        minute = datetime.datetime.strptime(minute, "%H:%M:%S") #Converts to needed datetime format
        x.append(minute)
    print("Graph Opening...")
    plt.plot(x, y, color=random.choice(['blue', 'olive', 'red', 'green', 'purple']), marker='.')


def plotBarGraph(averages: dict, title: str) -> None:
    style.use('Solarize_Light2')  # Sets style and labels
    plt.xlabel('Team')
    plt.ylabel('Sentiment Polarity (-1 -> 1)')
    plt.title(title)
    plt.bar(averages.keys(), averages.values(), color=random.choice(['blue', 'olive', 'red', 'green', 'purple']))

def plotCorrelation(averages : List, results : List) -> None:
    style.use('Solarize_Light2')  #Sets style and labels
    plt.ylabel('Goal Difference')
    plt.xlabel('Sentiment Polarity (-1 -> 1)')
    plt.scatter(averages, results, color=random.choice(['blue', 'olive', 'red', 'green', 'purple']))
    plt.plot(np.unique(averages), np.poly1d(np.polyfit(averages, results, 1))(np.unique(averages)))

def frequencyAnalyse(polarised_tweets : Dict):
    positive_words = {}
    negative_words = {}
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = list(stopwords.words('english'))
    for i in polarised_tweets:
        word_pit =  tokenizer.tokenize(polarised_tweets[i][0])
        tags = nltk.pos_tag(word_pit)
        for word in tags:
            if word[0] in positive_words:
                positive_words[word[0]] += 1
                continue
            elif word[0] in negative_words:
                negative_words[word[0]] += 1
                continue
            if len(word[0]) < 3:
                continue
            if word[0].lower() in stop_words:
                continue
            if word[1] in ['JJ']:
                if polarised_tweets[i][1] > 0.2:  #Positive
                    positive_words[word[0].lower()] = 1
                elif polarised_tweets[i][1] < -0.2:  #Negative
                    negative_words[word[0].lower()] = 1
    for w in sorted(negative_words, key=negative_words.get, reverse=True):
        print(w, negative_words[w])
    return (positive_words, negative_words)


def wordCloudGenerator(word_group : List, mask):
    wc = WordCloud(background_color="white", max_words=2000, mask=mask)
    clean_string = ','.join(word_group)
    wc.generate(clean_string)
    f = plt.figure(figsize=(200, 200))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()
