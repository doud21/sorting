"""sort.py: Sorts Tweets from Twitter with Python."""

from __future__ import unicode_literals
import os
import tweepy
from tkinter import *
import re
from textblob import TextBlob
import pandas as pd


#Obtaining keys from an Anaconda environment

consumerKey = os.environ.get("API_KEY")
consumerSecret = os.environ.get("SECRET_KEY")
accessToken = os.environ.get("TOKEN")
accessTokenSecret = os.environ.get("TOKEN_SECRET")


#Dev authentication to use API

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)


#Building the GUI for user input using the Tkinter interface

main = Tk()

L1 = Label(main, text="Starting Date in YYYY-MM-DD Format")
E1 = Entry(main)

L2 = Label(main, text="Number of Tweets to Display*")
E2 = Entry(main)

L3 = Label(main, text="Sort By Subjectivity")
E3 = Listbox(main, height=2, exportselection=0)
[E3.insert(END, item) for item in ["objective", "subjective"]]

L4 = Label(main, text="Sort By Polarity")
E4 = Listbox(main, height=2, exportselection=0)
[E4.insert(END, item) for item in ["positive", "negative"]]

N = Label(main, text="* = Required Question")


#Obtaining user input

def getData():
    date = E1.get()
    date = str(date)

    number = E2.get()
    number = int(number)

    valueSubjectivity = E3.get(ANCHOR)
    valueSubjectivity = str(valueSubjectivity)

    valuePolarity = E4.get(ANCHOR)
    valuePolarity = str(valuePolarity)

    # Pulls up coronavirus tweets in the last month

    search_terms = "coronavirus OR corona OR covid19 OR #coronavirus OR #corona OR #covid19"

    tweets = tweepy.Cursor(api.search, q=search_terms, lang="en", since=date).items(number)
    data_columns = [[tweet.user.screen_name, tweet.user.location, tweet.text] for tweet in tweets]
    tweet = pd.DataFrame(data=data_columns, columns=['user', 'location', 'tweet'])

    #Removes extraneous symbols and mentions from tweet

    def cleanTweet(text):
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'RT[\s]+', '', text)
        text = re.sub(r'https?:\/\/\S+', '', text)
        return text

    tweet['tweet'] = tweet['tweet'].apply(cleanTweet)

    #Gets polarity and subjectivity of tweet

    def getSubjectivity(text):
        if TextBlob(text).sentiment.subjectivity < 0.5:
            stringSubjectivity = "objective"
        else:
            stringSubjectivity = "subjective"
        return stringSubjectivity

    def getPolarity(text):
        if TextBlob(text).sentiment.polarity < 0.0:
            stringPolarity = "negative"
        else:
            stringPolarity = "positive"
        return stringPolarity

    tweet['subjectivity'] = tweet['tweet'].apply(getSubjectivity)
    tweet['polarity'] = tweet['tweet'].apply(getPolarity)


    if valueSubjectivity == "objective":
        tweet = tweet.loc[tweet['subjectivity'] == "objective"]
    elif valueSubjectivity == "subjective":
        tweet = tweet.loc[tweet['subjectivity'] == "subjective"]

    if valuePolarity == "positive":
        tweet = tweet.loc[tweet['polarity'] == "positive"]
    elif valuePolarity == "negative":
        tweet = tweet.loc[tweet['polarity'] == "negative"]


    print(tweet)


submit = Button(main, text="Search for me!", command=getData)


#Displaying GUI
L1.pack()
E1.pack()
L2.pack()
E2.pack()
L3.pack()
E3.pack()
L4.pack()
E4.pack()
N.pack()
submit.pack(side=BOTTOM)

main.mainloop()
