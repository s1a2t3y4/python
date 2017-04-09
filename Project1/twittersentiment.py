'''
Created on Apr 9, 2017

@author: satya
'''
import tweepy
from textblob import TextBlob



consumer_key= '8jEV89CFqoA8uh8SXhvk7NHG5'
consumer_secret='LOdxMEabXcRH0sUexizITX2SQtQsb6vSkqhlgQhSg3x8YUlUwu'

acess_token='202135894-WbIU3X5uhv1Mn7QQ0vBR5uU0lSDjb00Ny1UbG9JF'
acess_token_secret='V1OtjgRVFoleHHhxSpI2RAObvnjoRHPSyjkyFeALYz1i9'

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(acess_token,acess_token_secret)

api=tweepy.API(auth)

public_tweets=api.search('Trump')

for tweet in public_tweets:
    analysis=TextBlob(tweet.text)
    print(analysis.sentiment)