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
    print(colors.good + " Correctly saved information...\n" + colors.end)


def readCredentials(credentialsFile):
    try:
        data = []
        with open(credentialsFile) as json_file:
            data = json.load(json_file)
        json_file.close()
    except Exception as e:
        print(colors.bad + " Incorrect JSON format" + colors.end)
        sys.exit()

    return data

def instagramParameters(args,ig_username,ig_password):
    results = []
    api = InstagramAPI(ig_username,ig_password)

    if (api.login()):
        print(colors.good + " Login Success!\n" + colors.end)
        if args.info:
            instagram.getLocationID(api,args.info)

        if args.hashtag:
            results.extend(instagram.getUsersFromAHashTag(api,args.hashtag))

        if args.target:
            temp = instagram.getUserInformation(api,args.target)
            if temp == False:
                print(colors.info + " The user has a private profile or doesn't have public email..." + colors.end)
            else:
                results.extend(temp)
                if args.followers and not args.followings:
                    results.extend(instagram.getUserFollowers(api,args.target))
                if args.followings and not args.followers:
                    results.extend(instagram.getUserFollowings(api,args.target))
                if args.followers and args.followings:
                    followers = instagram.getUserFollowers(api,args.target)
                    followings =  instagram.getUserFollowings(api,args.target)
                    results.extend(instagram.sortContacts(followers,followings))
              
        if args.location:
            results.extend(instagram.getUsersFromLocation(api,args.location))

        if args.search_user:
            results.extend(instagram.getUsersOfTheSearch(api,args.search_user))
            
        if args.my_followers and not args.my_followings:
            results.extend(instagram.getMyFollowers(api))
            
        if args.my_followings and not args.my_followers:
            results.extend(instagram.getMyFollowings(api))
            
        if args.my_followings and args.my_followers:
            followers = instagram.getMyFollowers(api)
            followings = instagram.getMyFollowings(api)
            results.extend(instagram.sortContacts(followers,followings))  
    else:
        print(colors.bad + " Can't Login to Instagram!" + colors.end)
        #sys.exit()

    return results
    

def linkedinParameters(args,in_email,in_password):
    
    results = []
    api = Linkedin(in_email, in_password)
    if api.__dict__.get("success"):

        if args.company:
            linkedin.getCompanyInformation(api,args.company)
            users = []
            if args.employees:
                users = linkedin.getEmployeesFromCurrentCompany(api,args.company)
                results.extend(linkedin.getEmailsFromUsers(api,users))
            if args.employees and args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)


        if args.search_companies:
            companies = linkedin.searchCompanies(api,args.search_companies)
            users = []
            if args.employees:
                users = linkedin.getCompanyEmployees(api,companies)
                results.extend(linkedin.getEmailsFromUsers(api, users))
            if args.add_contacts and args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)

        if args.my_contacts:
            results.extend(linkedin.getEmailsFromUsers(api,linkedin.getMyContacts(api)))

        if args.user_contacts:
            results.extend(linkedin.getEmailsFromUsers(api,linkedin.getFollowers(api,args.user_contacts)))

        if args.search_users:
            users = linkedin.searchUsers(api,args.search_users)
            if args.pwndb:
                results.extend(linkedin.getEmailsFromUsers(api, users))
            if args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)
        
        if args.add_a_contact:
            linkedin.sendContactRequest(api,args.add_one_contact)

    else:
        print(colors.bad + " Can't Login to linkedin!" + colors.end)      

    return results
        
def run(args):

    results = []
    creds = ''
    if args.credentials and os.path.isfile(args.credentials) and os.access(args.credentials, os.R_OK):
        creds = readCredentials(args.credentials)
    else:
        print(colors.bad + " The file can't be accessed" + colors.end)
        sys.exit()

    if args.output and not os.path.isfile(args.output):
        print(colors.bad + " The file doesn't exist" + colors.end)
        sys.exit()
    
    if args.pwndb:
        status = os.system('systemctl is-active --quiet tor')
        if status != 0:
            print(colors.bad + " Can't connect to service! restart tor service and try again." + colors.end)
            sys.exit()

    if args.instagram:
        ig_username = creds.get("instagram").get("username")
        ig_password = creds.get("instagram").get("password")
        results.extend(instagramParameters(args,ig_username,ig_password))

    if args.linkedin:
        in_email = creds.get("linkedin").get("email")
        in_password = creds.get("linkedin").get("password")
        results.extend(linkedinParameters(args,in_email,in_password))
    
    if args.output:
        saveResults(args.output,results)

    if args.pwndb and results != [] and results != False:
        juicyInformation = PwnDB.findLeak(results)
        PwnDB.saveResultsPwnDB(juicyInformation)
    elif results == []:
        print(colors.info + " No emails were found to search." + colors.end)




