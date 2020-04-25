#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twint


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
    limit = 10,
    count = None,
    to = None,
    all_tweets = None,
    followers = None,
    followings = None,
    proxy_host = None,
    proxy_port = None,
    user_full = None,
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
    if followers:
        c.Followers = followers
    if followings:
        c.Following = followings
    if proxy_host:
        c.Proxy_host = proxy_host
    if proxy_port:
        c.Proxy_port = proxy_port
    if user_full:
        c.User_full = user_full
    if profile_full:
        c.Profile_full = profile_full
    
    # c.Search = "covid"
    # c.Limit = 5
    # c.Email = True
    # #c.Store_json = True
    # #c.Output = "result.txt"

    c.Store_object = True
    c.Store_object_tweets_list = tweets

    # Run
    twint.run.Search(c)

    return getListOfTweets(tweets)     

def getListOfTweets(tweets):
    results = []
    for tweet in tweets:
        results.append(tweet.__dict__)
    return results