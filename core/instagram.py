#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, requests, argparse, json, re, os, time
from core.colors import colors
from lib.InstagramAPI import InstagramAPI
from lib.PwnDB import PwnDB
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def getEmailsFromListOfUsers(api,items):
    targets = []
    print(colors.info + " Searching users... :) \n" + colors.end)
    
    for item in items:

        user = str(item.get("user").get("username"))
        targets.append(getUserProfile(api,user))

    return getEmailsFromUsers(api,targets)

def getUserProfile(api,username):

        print(colors.info + " Getting information from the user: " + str(username) + colors.end)
        time.sleep(float(0.5))
        api.searchUsername(username)

        if api.LastResponse.status_code == 429:
            print(colors.bad + " The request was not successful for the user: " + colors.W + username + colors.R + ". Maybe you should increase the delay" + colors.end)
        
        return api.LastJson

def getEmailsFromUsers(api,users):

    targets = []
    print(colors.info + " Searching users with emails :) \n" + colors.end)
    
    for user in users:
        if str(user["status"]) == "ok":

            username = str(user["user"].get("username"))
            userID = str(user["user"].get("pk"))
            email = str(user["user"].get("public_email"))
            followers = str(user["user"].get("follower_count"))
            following = str(user["user"].get("following_count"))
            biography = user["user"].get("biography").split(" ")
            private = str(user["user"].get("is_private"))
            
            if email != "None" and email !="":
                targets.append(json.dumps({"user":username,"userID":userID,"email":email,"private":private}))
                print(colors.good + " Username: " + colors.W + username + colors.B + " UserID: " + colors.W + userID + colors.B + " Email: " + colors.W + email + colors.B + " Followers: " + colors.W + followers + colors.B + " Following: " + colors.W + following + colors.end)
            else:
                result = searchEmailInBio(biography)
                if result:
                    print(colors.info + " The email was found in the user's biography: " + result + colors.end)
                    print(colors.good + " Username: " + colors.W + username + colors.B + " UserID: " + colors.W + userID + colors.B + " Email: " + colors.W + result + colors.B + " Followers: " + colors.W + followers + colors.B + " Following: " + colors.W + following + colors.end)
                    targets.append(json.dumps({"user":username,"userID":userID,"email":result,"private":private}))

    return list(set(targets))

def searchEmailInBio(bio):
    
    for word in bio:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',word):
            return word

def getLocationID(api,location):
    
    api.searchLocation(location)
    items = api.LastJson["items"]
    for item in items:
        print(colors.good + " City: " + colors.W + item.get("location").get("name") + colors.B +" Search ID: " + colors.W + str(item.get("location").get("pk")) + colors.end)

def getUsersFromAHashTag(api,hashtag):
    api.getHashtagFeed(hashtag)
    return getEmailsFromListOfUsers(api,api.LastJson["items"])

def getUsersFromLocation(api,locationId):
    api.getLocationFeed(locationId)
    return getEmailsFromListOfUsers(api,api.LastJson["items"])

def getUserInformation(api,target):
    userInfo = []
    api.searchUsername(str(target))
    info = api.LastJson
    userInfo.append(info)
    results = getEmailsFromUsers(api,userInfo)
    if not results == []:
        return results
    else:
        return info

def getUsersOfTheSearch(api,query):

    api.searchUsers(query)
    users = api.LastJson["users"]
    results = []

    for user in users:  
        api.searchUsername(user.get("username"))
        results.append(api.LastJson)
        userInfo = api.LastJson["user"]
        print(colors.good + " Username: " + colors.W + user.get("username") + colors.B + " User ID: " + colors.W + str(user.get("pk")) + colors.B + " Private: " + colors.W + str(user.get("is_private")) + colors.B + " Followers: " + colors.W + str(userInfo.get("follower_count")) + colors.B + " Following: " + colors.W + str(userInfo.get("following_count")) + colors.end)
    
    return results

def getMyFollowers(api):
    users = api.getTotalSelfFollowers()
    return getListOfUsers(api,users)

def getMyFollowings(api):

    users = api.getTotalSelfFollowings()
    return getListOfUsers(api,users)

def getUserFollowers(api,userID):

    users = api.getTotalFollowers(userID)
    return getListOfUsers(api,users)

def getUserFollowings(api,userID):
    
    users = api.getTotalFollowings(userID)
    return getListOfUsers(api,users)

def getListOfUsers(api,users):
    targets = []
    print(colors.info + " " + str(len(users)) + " targets have been obtained" + colors.end)

    for user in users:
        targets.append(getUserProfile(api,user.get("username")))
        
    return getEmailsFromUsers(api,targets)

def sortContacts(followers,followings):

    followers.extend(followings)
    targets = []

    for user in followers:
        temp = json.loads(user)
        targets.append(json.dumps({"user":temp.get("user"),"userID":temp.get("userID"),"email":temp.get("email"),"private":temp.get("private")}))
    return list(set(targets))

def saveResults(file,results):
    print(colors.info + " Writing the file..." + colors.end)
    content = ""
    with open(str(file), "r") as resultFile:
        content = resultFile.read()
    resultFile.close()
    with open(str(file), "a") as resultFile:
        for result in results:
            target = json.loads(result)
            if target['email'] not in content:
                resultFile.write(target['user']+":"+target['userID']+":"+target['email']+"\n")
    resultFile.close()
    print(colors.good + " Correctly saved information..." + colors.end)
    