# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:04:01 2018

@author: OpenSource
"""
#importing required library
import json
import matplotlib.pyplot as plt
import pandas as pd
import re #regular expression library
import numpy as np
from googletrans import Translator


#translator = Translator()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Reading Data

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

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Initializing empty list to store only required fields
list_text=[]
list_creat_time=[]
list_location=[]
list_favcount=[]
list_follwers_count=[]
list_lang=[]
#function to return value by getting a key
def extractdata(pos,key):
    
    x=tweets_data[pos]
    if ('user' in x): #trying to handle rough data
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
        


#looping for dimensionality reduction
for i in range(len(tweets_data)):
    
    list_text.append(extractdata(i,'text'))
    list_creat_time.append(extractdata(i,'created_at'))
    list_location.append(extractdata(i,'location'))
    list_favcount.append(extractdata(i,'favourites_count'))
    list_follwers_count.append(extractdata(i,'followers_count'))
    list_lang.append(extractdata(i,'lang'))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    

#convert those extracted list to Dataframe
dr_tweet_df = pd.DataFrame({'text':list_text,'language':list_lang,'created_at':list_creat_time,'location':list_location,'fav_count':list_favcount,'followers_count':list_follwers_count})         

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#remove blank row in dataframe
z=[]
for i in range (len(list_text)):
    if (list_text[i]==''):
        z.append(i)

for i in range (len(z)):
    dr_tweet_df.drop(dr_tweet_df.index[z[i]-i], inplace=True)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Some basic data analytics.Showing the bar plot according to language and area

tweets_by_lang = dr_tweet_df['language'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='#794bc4')    

# some analytics
tweets_by_location = dr_tweet_df['location'].value_counts()
#showing top 5 no of tweets according to location
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('location', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 3 location', fontsize=15, fontweight='bold')
tweets_by_location[:3].plot(ax=ax, kind='bar', color='#794bc4') 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Basic statistics
tweets_by_lang = dr_tweet_df['language'].value_counts()
dr_tweet_df['followers_count'].mean() #mean of total follower counts
dr_tweet_df
dr_tweet_df=dr_tweet_df.reset_index()
dr_tweet_df.head
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Free google translation API
'''  
#translation using google free API
import goslate   
text = "Hello World"

gs = goslate.Goslate()
translatedText = gs.translate(text,'fr')
translatedText

dr_tweet_df['text'][6]
translatedText = gs.translate(dr_tweet_df['text'][6],'en')
translatedText

temp=[]

for i in range (len(dr_tweet_df['language'])):
    if (dr_tweet_df['language'][i] != "en"):
        translatedText = trans(dr_tweet_df['text'][i])
        temp.append(translatedText)
        print(translatedText)
        
        
def trans(txt):
        translatev = gs.translate(txt,'en') 
        return translatev


import pydeepl
sentence = 'I like turtles.'
from_language = 'ja'
to_language = 'EN'
# Using auto-detection
translation = pydeepl.translate(dr_tweet_df['text'][6],from_language, to_language)
print(translation)
'''
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


#### Google Cloud Translator

#Imports the Google Cloud client library
from google.cloud import translate

#Instantiates a client
translate_client = translate.Client()
# The target language
target = 'en'

### An example
text=dr_tweet_df['text'][6]

#Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target)

print(u'Text: {}'.format(dr_tweet_df['text'][6]))
print(u'Translation: {}'.format(translation['translatedText']))

#Now converting all other language text
temp=[]
temp1=dr_tweet_df['text'].tolist()
def trans(txt):
        translatev = translate_client.translate(txt,target_language=target)
        return translatev
x=0
for i in range (len(dr_tweet_df['language'])):
    x=x+1
    if (dr_tweet_df['language'][i] == "hi"):
        translatedText = trans(dr_tweet_df['text'][i])
        temp1[i] = translatedText['translatedText']
        
      
        
x=0
for i in range (len(dr_tweet_df['language'])):
    x=x+1
    if (dr_tweet_df['language'][i] != "en"):
        translatedText = trans(dr_tweet_df['text'][i])
        temp1[i] = translatedText['translatedText']
        
dr_tweet_df['text']=pd.Series(temp1) # updating translated text in dataframe

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

##---------------------prioritizing
        
## Prioritization
## dropping tweet based on their like and followers
#remove blank row in dataframe
z=[]
x=0
for i in range (len(dr_tweet_df['fav_count'])):
    if (dr_tweet_df['fav_count'][i]<=100 and dr_tweet_df['followers_count'][i]<=30 ):
        z.append(i)


for i in range (len(z)):
        #dr_tweet_df.drop(dr_tweet_df.index[i])
        dr_tweet_df.drop(dr_tweet_df.index[z[i]-i], inplace=True)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
##-----------------------valid word detection ,url removal,emoji removal
def clean_tweet(tweet):
    clean_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with ''
    tweet = remove_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        clean_tweet.append(word)

    return ' '.join(clean_tweet)

def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # tryyyy --> try
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word
#removing emoji
def remove_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', '', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', '', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', '', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', '', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', '', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', '', tweet)
    return tweet

var_tweet=dr_tweet_df['text'].tolist()
var_cln_tweet=[]
for i in var_tweet:
    var_cln_tweet.append(clean_tweet(i))
    

dr_tweet_df['text']=pd.Series(var_cln_tweet)    






















        