#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json
from lib.InstagramAPI import InstagramAPI
from lib.PwnDB import PwnDB
from core import instagram
from core.colors import colors

def run(args):
    
    if args.output and not os.path.isfile(args.output):
        print(colors.bad + "The file doesn't exist")
        sys.exit()

    api = InstagramAPI(args.user,args.password)
    print(args)
    if (api.login()):
        print(colors.good + " Login Success!\n")
        if args.info:
            instagram.getLocationID(api,args.info)

        if args.hashtag:
            results = instagram.getUsersFromAHashTag(api,args.hashtag)

        if args.target:
            results = instagram.getUserInformation(api,args.target)
            if len(results) > 1:
                print(colors.info + " The user has a private profile or doesn't have public email..." + colors.end)
                if args.followers and not args.followings:
                    results = instagram.getUserFollowers(api,str(results["user"].get("pk")))
                if args.followings and not args.followers:
                    results = instagram.getUserFollowings(api,str(results["user"].get("pk")))
                if args.followers and args.followings:
                    followers = instagram.getUserFollowers(api,str(results["user"].get("pk")))
                    followings =  instagram.getUserFollowings(api,str(results["user"].get("pk")))
                    results = instagram.sortContacts(followers,followings)
            else:
                temp = json.loads(results[0])
                if args.followers and temp.get("private") == "False" and not args.followings:
                    results = instagram.getUserFollowers(api,str(temp.get("userID")))
                
                if args.followings and temp.get("private") == "False" and not args.followers:
                    results = instagram.getUserFollowings(api,str(temp.get("userID")))
                if args.followings and args.followers and temp.get("private") == "False":
                    followers = instagram.getUserFollowers(api,str(temp.get("userID")))
                    followings =  instagram.getUserFollowings(api,str(temp.get("userID")))
                    results = instagram.sortContacts(followers,followings)

            
        if args.location:
            results = instagram.getUsersFromLocation(api,args.location)

        if args.search_user:
           temp = instagram.getUsersOfTheSearch(api,args.search_user)
           if args.pwndb and temp != []:
               results = instagram.getEmailsFromUsers(api,temp)
        
        if args.my_followers and not args.my_followings:
            results = instagram.getMyFollowers(api)
        
        if args.my_followings and not args.my_followers:
            results = instagram.getMyFollowings(api)
        
        if args.my_followings and args.my_followers:
            followers = instagram.getMyFollowers(api)
            followings = instagram.getMyFollowings(api)
            results = instagram.sortContacts(followers,followings)

        if args.output:
            instagram.saveResults(args.output,results)
        if args.pwndb and len(results) > 0:
            juicyInformation = PwnDB.findLeak(results)
            PwnDB.saveResultsPwnDB(juicyInformation)    
    else:
        print(colors.bad + " Can't Login!\n")
        sys.exit()