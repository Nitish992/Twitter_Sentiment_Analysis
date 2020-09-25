#Import Libaries
import tweepy
from textblob import TextBlob
import pandas as pd
import re

#Twitter API Credentials
#Paste your keys here.
#To get your API keys sign in to Twitter Developer. https://developer.twitter.com/en
consumerKey = "vzJnHEXhsatqg5tgjVft1tdeA"
consumerSecret = "mZCHzvs780829lOX1vFsYW8pMGJMO1h2NbL1ML3NufBWxEIgp6" 
accessToken = "3699213675-NDACEg5OllUloBypgZGoyxE7uY8FF6sHBc2y3NH"
accessTokenSecret = "PLtHnAMevgM09ll4wVm58CMCTtbV8ERA9pWUbwwAGGLYo"

#Auth
authenticate = tweepy.OAuthHandler(consumerKey,consumerSecret)
authenticate.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

#Extract Tweets
#In screen_name enter the twitter username of the person you want to analyse sentiment.
#In count enter the number of tweets you want to analyse.
posts = api.user_timeline(screen_name = "NarendraModi", count=50, lang="en", tweet_mode="extended")

#Create dataframe
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
#df.head()

#Cleaning the tweets
def clean(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text)
  text = re.sub(r'#', '', text)
  text = re.sub(r'RT[\s]+', '', text)
  text = re.sub(r'https:\/\/S', '', text)

  return text

df['Tweets']= df['Tweets'].apply(clean)
#df.head() 

#Subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

#Polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

#Create columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
#df

#Calculate Positive, Negative and Neutral
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'
df['Analysis'] = df['Polarity'].apply(getAnalysis)
print(df)

