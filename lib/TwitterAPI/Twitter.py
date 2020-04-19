#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twint

def getTweets():

    tweets = []
    # Configure
    c = twint.Config()
    c.Search = "covid"
    c.Limit = 5000
    #c.Store_json = True
    #c.Output = "result.txt"

    c.Store_object = True
    c.Store_object_tweets_list = tweets

    # Run
    twint.run.Search(c)

    print("===========")
    print(tweets)
    for tweet in tweets:
        print(tweet)
