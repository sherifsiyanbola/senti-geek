#Sentiment Analysis and Visualisation of public reaction on Twitter about products or news using NLP
import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi

if sys.version_info[0] < 3:
   input = raw_input

# keys and tokens from the Twitter Dev Console 
consumer_key = 'WnGTlknZiA91x8xtmkeOf0Qrz'
consumer_secret = '1xX1C9tQRIPlXzjomg3nrHMoXKph6z5dbHc3FjkJbTR079J6cr'
access_token = '824983274-JwfopAu0kxX4iuHc6mJDRT11Zims8sES3cX9Vsko'
access_token_secret = '0OthCQ2X1ZIj3szAzsNa16E7r00KnmGY3lEbYp6hW6Mhp'

## AYLIEN credentials
application_id = "51e5aa43"
application_key = "5030096c9781a63e74b9d53bb018c512"

## set up an instance of Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## set up an instance of the AYLIEN Text API
client = textapi.Client(application_id, application_key)

## search Twitter for something that interests you
query = input("What subject do you want to analyze for this example? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(
   lang="en",
   q=query + " -rt",
   count=number,
   result_type="recent"
)

print("--- Gathered Tweets \n")

## open a csv file to store the Tweets and their sentiment 
file_name = '/media/geek/01D3DD7B131B52B0/geek.py/Geek-NLP/TSA/Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)

with open(file_name, 'w') as csvfile:
   csv_writer = csv.DictWriter(
       f=csvfile,
       fieldnames=["Tweet", "Sentiment", "Confidence"]
   )
   csv_writer.writeheader()

   print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

## tidy up the Tweets and send each to the AYLIEN Text API
   for c, result in enumerate(results, start=1):
       tweet = result.text
       tidy_tweet = tweet.strip().encode('ascii', 'ignore')

       if len(tweet) == 0:
           print('Empty Tweet')
           continue

       response = client.Sentiment({'text': tidy_tweet})
       csv_writer.writerow({
           'Tweet': response['text'],
           'Sentiment': response['polarity'],
           'Confidence': response['polarity_confidence']
       })

       print("Analyzed Tweet {}".format(c))

## count the data in the Sentiment column of the CSV file 
with open(file_name, 'r') as data:
   counter = Counter()
   for row in csv.DictReader(data):
       counter[row['Sentiment']] += 1

   positive = counter['positive']
   negative = counter['negative']
   neutral = counter['neutral']

## declare the variables for the pie chart, using the Counter variables for "sizes"
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(
   x=sizes,
   shadow=True,
   colors=colors,
   labels=labels,
   startangle=90
)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
plt.show()