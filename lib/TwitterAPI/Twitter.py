#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twint
from core.colors import colors


def getTweets(
    username = None,
    search = None,
    year = None,
    since = None,
    until = None,
    email = True,
    phone = None,
    verified = None,
    hashtags = None,
    userid = None,
    limit = 100,
    count = None,
    to = None,
    all_tweets = None,
    profile_full = None
    ):

    tweets = []
    # Configure
    c = twint.Config()
    c.Limit = limit
    c.Email = email

    if username:
        c.Username = username
    if search:
        c.Search = search
    if year:
        c.Year = year
    if since:
        c.Since = since
    if until:
        c.Until = until
    if phone:
        c.Phone = phone
    if verified:
        c.Verified = verified
    if hashtags:
        c.Hashtags = hashtags
    if userid:
        c.User_id = userid
    if count:
        c.Count = count
    if to:
        c.To = to
    if all_tweets:
        c.All = all_tweets
    if profile_full:
        c.Profile_full = profile_full
    
    c.Store_object = True
    c.Store_object_tweets_list = tweets

    # Run
    twint.run.Search(c)
    
    return getListOfTweets(tweets)
    
def getFollowers(
    username,
    limit = 100
    ):  
    
    users = []

    c = twint.Config()
    c.Username = username
    c.Limit = limit
    c.Store_object = True
    twint.run.Followers(c)
    users = twint.output.follows_list
    return users

def getFollowings(
    username,
    limit = 100
    ):
    
    users = []

    c = twint.Config()
    c.Username = username
    c.Limit = limit
    c.Store_object = True
    twint.run.Following(c)
    users = twint.output.follows_list
    return users


def getUserInformation(username):
    print(colors.good + " Getting the information from the user: " + username + "\n" + colors.W)
    c = twint.Config()
    c.Username = username
    twint.run.Lookup(c)
    print("\n"+colors.end)

def getListOfTweets(tweets):
    results = []
    for tweet in tweets:
        results.append(tweet.__dict__)
    return results