# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:04:01 2018

@author: OpenSource
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from googletrans import Translator
translator = Translator()

tweets_data_path = 'data1.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print (len(tweets_data))

list_text=[]
list_creat_time=[]
list_location=[]
list_favcount=[]
list_follwers_count=[]
list_lang=[]

#looping for dimensionality reduction
for i in range(len(tweets_data)):
    
    list_text.append(extractdata(i,'text'))
    list_creat_time.append(extractdata(i,'created_at'))
    list_location.append(extractdata(i,'location'))
    list_favcount.append(extractdata(i,'favourites_count'))
    list_follwers_count.append(extractdata(i,'followers_count'))
    list_lang.append(extractdata(i,'lang'))

#function to return value by getting a key
def extractdata(pos,key):
    
    x=tweets_data[pos]
    if ('user' in x): 
        if (key=='location' or key=='favourites_count' or key=='followers_count' or key=='list_lang'):
            y=x['user']
            return (y[key])
        else:
            if (key in x):
                return (x[key])
            else:
                return('')
    else:
        return('')
        

    

#convert those extracted list to Dataframe
dr_tweet_df = pd.DataFrame({'text':list_text,'language':list_lang,'created_at':list_creat_time,'location':list_location,'fav_count':list_favcount,'followers_count':list_follwers_count})         



#remove blank row in dataframe
z=[]
for i in range (len(list_text)):
    if (list_text[i]==''):
        z.append(i)

for i in range (len(z)):
    dr_tweet_df.drop(dr_tweet_df.index[z[i]-i], inplace=True)

tweets_by_lang = dr_tweet_df['language'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')    

# some analytics
tweets_by_location = dr_tweet_df['location'].value_counts()
#showing top 5 no of tweets according to location
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('location', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 3 location', fontsize=15, fontweight='bold')
tweets_by_location[:3].plot(ax=ax, kind='bar', color='red') 

#Basic statistics
tweets_by_lang = dr_tweet_df['language'].value_counts()
dr_tweet_df['followers_count'].mean() #mean of total follower counts
dr_tweet_df
dr_tweet_df=dr_tweet_df.reset_index()
dr_tweet_df

#-------------------------------------------------------------Example

#translation
import goslate

# Imports the Google Cloud client library
#from google.cloud import translate

# Instantiates a client
#translate_client = translate.Client()

# The text to translate
#text = u'Hello, world!'
# The target language
#target = 'ru'

# Translates some text into Russian
#translation = translate_client.translate(
    #text,
    #target_language=target)

#print(u'Text: {}'.format(text))
#print(u'Translation: {}'.format(translation['translatedText']))
    
    
text = "Hello World"

gs = goslate.Goslate()
translatedText = gs.translate(text,'fr')
translatedText

dr_tweet_df['text'][6]
translatedText = gs.translate(dr_tweet_df['text'][6],'en')
translatedText



##---------------------prioritizing
        
## Prioritization
## dropping tweet based on their like and followers
#remove blank row in dataframe
z=[]
for i in range (len(dr_tweet_df['fav_count'])):
    if (list_text[i]==''):
        z.append(i)
        
        list_favcount=[]
list_follwers_count=[]

for i in range (len(z)):
    dr_tweet_df.drop(dr_tweet_df.index[z[i]-i], inplace=True)