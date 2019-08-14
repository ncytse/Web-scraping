#https://www.earthdatascience.org/courses/earth-analytics/using-apis-natural-language-processing-twitter/intro-to-social-media-text-mining-python/
#https://www.earthdatascience.org/courses/earth-analytics-python/using-apis-natural-language-processing-twitter/get-and-use-twitter-data-in-python/

#Tweepy Documentation
#http://docs.tweepy.org/en/v3.6.0/index.html

#Twitter API
#https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators

#This Is How Twitter Sees The World : Sentiment Analysis Part One
#https://towardsdatascience.com/the-real-world-as-seen-on-twitter-sentiment-analysis-part-one-5ac2d06b63fb

#Twitter Sntiment Analysis
#https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed

import tweepy as tw
import pandas as pd
import datetime

agent_names=["Orca Pacific","Evolution Lighting LLC","Magid Safety","Central National-Gottesman","LF Products Pte Ltd"]
company_names=["Airisu Corporation","Freewill Sports Pvt Ltd","Brikhot Home Pvt Ltd","Apache Mills","Dorel Asia SRL"]


print('starting time', datetime.datetime.now().time())
#input keywords
query_list = ['Evolution','Lighting']
#https://twitter.com/search?f=news&vertical=default&q=china%2Btextile%2Bfactory&src=typd

#Key
consumer_key= 'xxxxxxxxxx'
consumer_secret= 'xxxxxxxxxx'
access_token= 'xxxxxxxxxx'
access_token_secret='xxxxxxxxxx'

search_words = "+".join(query_list) + "-filter:retweets"
date_since = "2017-1-1"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items()

L = [tweet.text for tweet in tweets]

# Iterate on tweets
#for tweet in tweets:
    #print(tweet.text)

"""
######To Keep or Remove Retweets######
#ignore all retweets    
new_search = search_words + " -filter:retweets"    
    
tweets = tw.Cursor(api.search, 
                           q=new_search,
                           lang="en",
                           since=date_since).items(n)    
    
users_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]    
users_locs
"""

df = pd.DataFrame(L, columns=['tweet'])
print (df)

#df.to_csv('out.csv',index=False)
df.to_csv('Twitter_Agent or company result/out-'+"+".join(query_list)+'.csv',index=False)

print('finishing time', datetime.datetime.now().time())
#Add time
#Add verified filter
#no of tweets and like
#Human Right
#Unicef, iLab, world bank
#new emergency issus, supply chain, risk, mediapresent force labour and commodity,which country?? 
#seafood for thailand, force labour in MY, prison labour in CN
#human right risk + all countries, force labour, food commodity/ textile ... after 2018
#no of results by country (no of verifed result)

