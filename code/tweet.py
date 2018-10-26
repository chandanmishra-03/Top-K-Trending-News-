# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "3716247554-7oIUwckI4o5NfyYP75JN3w6VtHXzMWzpYqUKi4A"
access_token_secret = "g93GfxibWTowQVMq5zOvYlricaOLxNMWFCaxQyoH3oVYG"
consumer_key = "e5e9gXT5gDnpL2c5Q4z70ooyJ"
consumer_secret = "JerAxl0mBzmMhmaeGhMFkydCEBhfCp2zK8FrgNKxyQhoWA2vH6"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.sample()
    