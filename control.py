from abstract_tweets import *
from basic_sentiment import *
from typing import *
from PIL import Image
import csv

class Analyse:
    def __init__(self):
        self._team_name : str
        self._file_name : str
        self._title : str
        self._kick_off_hour : int
        self._kick_off_minute: int
        self._result : int
        self._polarity : float
        self._image_file : str

    def setTeamName(self) -> None:
        self._team_name = input("TEAM NAME:\n>>>")

    def setFileName(self) -> None:
        self._file_name = input("Enter FILE NAME:\n>>>")

    def setGraphInfo(self) -> None:
        self._title = input("Enter the TITLE:\n>>>")
        self._kick_off_hour = int(input("Enter Kick-Off HOUR:\n>>>"))
        self._kick_off_minute = int(input("Enter Kick-Off MINUTE:\n>>>"))

    def setResult(self) -> None:
        self._result = int(input("Enter the goal difference (+x WIN, 0 DRAW ,-x LOSS):\n>>>"))

    def gatherTweets(self) -> Dict:
        tweets : List = gatherTweets(self._file_name)
        abstracted : Dict = abstractTweets(tweets)
        print(str(len(abstracted)) + " tweets accepted.")
        return abstracted

    def findSentiment(self, abstracted) -> Dict:
        polarised_tweets = getSentiment(abstracted)
        return polarised_tweets

    def calculateAverage(self, polarised_tweets : Dict) -> Tuple:
        return (self._team_name, findAverage(polarised_tweets))

    def createLineGraph(self, polarised_tweets : Dict) -> None:
        polarised_time = AverageByTime(polarised_tweets)
        plotGraph(polarised_time, self._kick_off_hour, self._kick_off_minute, self._title)
        plt.legend([self._team_name])

    def createBarChart(self, averages, title):
        plotBarGraph(averages, title)

    def setPolarity(self, polarised_tweets : Dict) -> None:
        self._polarity = findAverage(polarised_tweets)

    def getFrequency(self, polarised_tweets : Dict) -> Tuple:
        return frequencyAnalyse(polarised_tweets)

    def setImageFile(self):
        self._image_file = input("Enter name of the image:\n>>>")

def average():
    num_of_teams = int(input("Enter NUMBER of teams:\n>>>"))
    teams = [Analyse() for n in range(num_of_teams)]
    for t in teams:
        result = {}
        t.setTeamName()
        t.setFileName()
        while True:
            try:
                abstracted = t.gatherTweets()
                break
            except:
                print("file does not exist!")
                t.setFileName()
        polarised = t.findSentiment(abstracted)
        average = t.calculateAverage(polarised)
        result[average[0]] = average[1]
        t.createBarChart(result, title='PL')
    plt.show()


def graph():
    num_of_teams = int(input("Enter NUMBER of teams:\n>>>"))
    teams = [Analyse() for n in range(num_of_teams)]
    for t in teams:
        t.setTeamName()
        t.setFileName()
        t.setGraphInfo()
        while True:
            try:
                abstracted = t.gatherTweets()
                break
            except FileNotFoundError:
                print("file does not exist!")
                t.setFileName()
        polarised = t.findSentiment(abstracted)
        t.createLineGraph(polarised)
    plt.title("PL")
    plt.show()

def correlation():
    num_of_teams = int(input("Enter NUMBER of teams:\n>>>"))
    teams = [Analyse() for n in range(num_of_teams)]
    results = []
    averages = []
    for t in teams:
        t.setFileName()
        t.setResult()
        while True:
            try:
                abstracted = t.gatherTweets()
                break
            except FileNotFoundError:
                print("file does not exist!")
                t.setFileName()
        polarised = t.findSentiment(abstracted)
        t.setPolarity(polarised)
        results.append(t._result)
        averages.append(t._polarity)
    plotCorrelation(averages, results)
    #write to .csv
    file = open('C:/Users/Liam/desktop/correlation.csv', 'a')
    for i in range(len(averages)):
        text = str(averages[i]) + ',' + str(results[i]) + '\n'
        file.write(text)
    file.close()
    plt.show()

def frequencyAnalysis():
    team = Analyse()
    try:
        team.setFileName()
    except FileNotFoundError:
        print("file does not exist!")
        team.setFileName()
    abstracted = team.gatherTweets()
    polarised = team.findSentiment(abstracted)
    frequencies = team.getFrequency(polarised)
    positive_frequency = frequencies[0]
    negative_frequency = frequencies[1]
    print(positive_frequency)
    print(negative_frequency)
    print(len(positive_frequency))
    print(len(negative_frequency))
    return (positive_frequency, negative_frequency)

def wordCloud():
    team = Analyse()
    all_words = frequencyAnalysis()
    choice = input("Positive [p] or Negative [n] wordcloud?\n>>>")
    selected = False
    while not selected:
        if choice == 'p':
            words = all_words[0]
            selected = True
        elif choice == 'n':
            words = all_words[1]
            selected = True
    team.setImageFile()
    while True:
        try:
            mask = np.array(Image.open("C:/Users/Liam/Desktop/" + team._image_file))
            print("accepted!")
            break
        except FileNotFoundError:
            print("File not found!")
            team.setImageFile()
    wordCloudGenerator(words, mask)

def regression():
    polarity = []
    results = []
    with open('C:/Users/Liam/desktop/correlation.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            polarity.append(row[0])
            results.append(row[1])
    model = createModel(polarity, results)
    prediction = predictOutcome(model, float(input("Enter the pre-match polarity:\n>>>")))
    print(prediction)

if '__name__' != '__main__':
    choice = input("AVERAGE            : '1'\n"
                   "GRAPH              : '2'\n"
                   "CORRELATE          : '3'\n"
                   "FREQUENCY ANALYSIS : '4'\n"
                   "WORDCLOUD          : '5'\n"
                   "REGRESSION         : '6'\n"
                   ">>>")
    if choice == '1':
        average()
    elif choice =='2':
        graph()
    elif choice == '3':
        correlation()
    elif choice == '4':
        frequencyAnalysis()
    elif choice == '5':
        wordCloud()
    elif choice == '6':
        regression()
