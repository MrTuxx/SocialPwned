#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json
from lib.InstagramAPI import InstagramAPI
from lib.LinkedInAPI import Linkedin
from lib.PwnDB import PwnDB
from core import instagram
from core import linkedin
from core.colors import colors

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

def instagramParameters(args):
    results = ''
    api = InstagramAPI(args.user,args.password)

    if (api.login()):
        print(colors.good + " Login Success!\n" + colors.end)
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
    else:
        print(colors.bad + " Can't Login!")
        sys.exit()

    return results
    

def linkedinParameters(args):
    
    results = ''
    api = Linkedin(args.user, args.password)
    
    if args.company:
        linkedin.getCompanyInformation(api,args.company)
        users = []
        if args.employees:
            users = linkedin.getEmployeesFromCurrentCompany(api,args.company)
            results = linkedin.getEmailsFromUsers(api,users)
        if args.employees and args.add_contacts:
            linkedin.sendContactRequestAListOfUsers(api,users)


    if args.search_companies:
        companies = linkedin.searchCompanies(api,args.search_companies)
        users = []
        if args.employees:
            users = linkedin.getCompanyEmployees(api,companies)
            results = linkedin.getEmailsFromUsers(api, users)
        if args.add_contacts and args.add_contacts:
            linkedin.sendContactRequestAListOfUsers(api,users)

    if args.my_contacts:
        results = linkedin.getEmailsFromUsers(api,linkedin.getMyContacts(api))

    if args.user_contacts:
        results = linkedin.getEmailsFromUsers(api,linkedin.getFollowers(api,args.user_contacts))

    if args.search_users:
        users = linkedin.searchUsers(api,args.search_users)
        if args.pwndb:
            results = linkedin.getEmailsFromUsers(api, users)
        if args.add_contacts:
            linkedin.sendContactRequestAListOfUsers(api,users)
    
    if args.add_a_contact:
        linkedin.sendContactRequest(api,args.add_one_contact)


    return results
        
def run(args):

    results = []

    if args.output and not os.path.isfile(args.output):
        print(colors.bad + "The file doesn't exist")
        sys.exit()
    
    if args.pwndb:
        status = os.system('systemctl is-active --quiet tor')
        if status != 0:
            print(colors.bad + " Can't connect to service! restart tor service and try again." + colors.end)
            sys.exit()

    if args.instagram:
        results = instagramParameters(args)

    if args.linkedin:
        results = linkedinParameters(args)
    
    if args.output:
        saveResults(args.output,results)

    if args.pwndb and results != [] and results != False:
        juicyInformation = PwnDB.findLeak(results)
        PwnDB.saveResultsPwnDB(juicyInformation)
    elif results == []:
        print(colors.info + " No emails were found to search." + colors.end)




