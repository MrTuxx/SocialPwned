#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json
from lib.InstagramAPI import InstagramAPI
from lib.LinkedInAPI import Linkedin
from lib.PwnDB import PwnDB
from core import instagram
from core import linkedin
from core.colors import colors


def instagramParameters(args):

    if args.output and not os.path.isfile(args.output):
        print(colors.bad + "The file doesn't exist")
        sys.exit()
    
    if args.pwndb:
        status = os.system('systemctl is-active --quiet tor')
        if status != 0:
            print(colors.bad + " Can't connect to service! restart tor service and try again." + colors.end)
            sys.exit()
    api = InstagramAPI(args.user,args.password)
    #print(args)
    if (api.login()):
        print(colors.good + " Login Success!\n" + colors.end)
        results = ''
        if args.info:
            instagram.getLocationID(api,args.info)

        if args.hashtag:
            results = instagram.getUsersFromAHashTag(api,args.hashtag)

        if args.target:
            results = instagram.getUserInformation(api,args.target)
            if results == False:
                print(colors.info + " The user has a private profile or doesn't have public email..." + colors.end)
            else:
                if args.followers and not args.followings:
                    results = instagram.getUserFollowers(api,args.target)
                if args.followings and not args.followers:
                    results = instagram.getUserFollowings(api,args.target)
                if args.followers and args.followings:
                    followers = instagram.getUserFollowers(api,args.target)
                    followings =  instagram.getUserFollowings(api,args.target)
                    results = instagram.sortContacts(followers,followings)
            
        if args.location:
            results = instagram.getUsersFromLocation(api,args.location)

        if args.search_user:
           results = instagram.getUsersOfTheSearch(api,args.search_user)
        
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
    
        if args.pwndb and results != [] and results != False:
            juicyInformation = PwnDB.findLeak(results)
            PwnDB.saveResultsPwnDB(juicyInformation)
        elif results == []:
            print(colors.info + " No emails were found to search." + colors.end)
    else:
        print(colors.bad + " Can't Login!")
        sys.exit()
    

def linkedinParameters(args):
    
    if args.linkedin:

        api = Linkedin(args.user, args.password)
        
        results = ''
        
        if args.company:
            linkedin.getCompanyInformation(api,args.company)

        if args.search_companies:
            companies = linkedin.searchCompanies(api,args.search_companies)
            if args.employees:
                results = linkedin.getEmailsFromCompanyEmployees(api,companies)
        
        if args.pwndb and results != [] and results != False:
            juicyInformation = PwnDB.findLeak(results)
            PwnDB.saveResultsPwnDB(juicyInformation)
        elif results == []:
            print(colors.info + " No emails were found to search." + colors.end)

def run(args):

    if args.instagram:
        instagramParameters(args)

    if args.linkedin:
        linkedinParameters(args)
    






