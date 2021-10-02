#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, datetime
from lib.InstagramAPI import InstagramAPI
from lib.LinkedInAPI import Linkedin
from lib.PwnDB import PwnDB
from lib.Dehashed import DehashedAPI
from core import instagram
from core import linkedin
from core import twitter
from core import ghunt
from core import output
from core.colors import colors

def readCredentials(credentialsFile):
    try:
        data = []
        with open(credentialsFile) as json_file:
            data = json.load(json_file)
        json_file.close()
    except:
        print(colors.bad + " Incorrect JSON format" + colors.end)
        sys.exit()

    return data

def instagramParameters(args,ig_username,ig_password):
    results = []
    api = InstagramAPI(ig_username,ig_password)

    if (api.login()):
        print(colors.good + " Successful login to Instagram!\n" + colors.end)
        if args.info:
            instagram.getLocationID(api,args.info)

        if args.hashtag_ig:
            results.extend(instagram.getUsersFromAHashTag(api,args.hashtag_ig))

        if args.target_ig:
            temp = instagram.getUserInformation(api,args.target_ig)
            if temp == False:
                print(colors.info + " The user has a private profile or doesn't have public email..." + colors.end)
            else:
                results.extend(temp)
                if args.followers_ig and not args.followings_ig:
                    results.extend(instagram.getUserFollowers(api,args.target_ig))
                if args.followings_ig and not args.followers_ig:
                    results.extend(instagram.getUserFollowings(api,args.target_ig))
                if args.followers_ig and args.followings_ig:
                    followers = instagram.getUserFollowers(api,args.target_ig)
                    followings =  instagram.getUserFollowings(api,args.target_ig)
                    results.extend(instagram.sortContacts(followers,followings))
              
        if args.location:
            results.extend(instagram.getUsersFromLocation(api,args.location))

        if args.search_users_ig:
            results.extend(instagram.getUsersOfTheSearch(api,args.search_users_ig))
            
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

    return results
    

def linkedinParameters(args,in_email,in_password,out_dir):
    
    results = []
    api = Linkedin(in_email, in_password)
    if api.__dict__.get("success"):
        print(colors.good + " Successful login to Linkedin!\n" + colors.end)
        
        if args.company:
            linkedin.getCompanyInformation(api,args.company)
            users = []
            if args.employees:
                users = linkedin.getEmployeesFromCurrentCompany(api,args.company)
                output.linkedin2usernames(users,out_dir)
                results.extend(linkedin.getEmailsFromUsers(api,users))
            if args.employees and args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)

        if args.search_companies:
            companies = linkedin.searchCompanies(api,args.search_companies)
            users = []
            if args.employees:
                users = linkedin.getCompanyEmployees(api,companies)
                output.linkedin2usernames(users,out_dir)
                results.extend(linkedin.getEmailsFromUsers(api, users))
            if args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)

        if args.my_contacts:
            results.extend(linkedin.getEmailsFromUsers(api,linkedin.getMyContacts(api)))

        if args.user_contacts:
            users = linkedin.getFollowers(api,args.user_contacts)
            results.extend(linkedin.getEmailsFromUsers(api,users))
            if args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)

        if args.search_users_in:
            users = linkedin.searchUsers(api,args.search_users_in)
            if args.pwndb:
                results.extend(linkedin.getEmailsFromUsers(api, users))
            if args.add_contacts:
                linkedin.sendContactRequestAListOfUsers(api,users)

        if args.target_in:
            results.extend(linkedin.getUserInformation(api,args.target_in))
            if args.add_contacts:
                linkedin.sendContactRequest(api,args.target_in)

        if args.add_a_contact:
            linkedin.sendContactRequest(api,args.add_one_contact)

    else:
        print(colors.bad + " Can't Login to linkedin!" + colors.end)      

    return results

def twitterParameters(args):
    results = []
    print(colors.good + " Using Twint!\n" + colors.end)

    if args.target_tw and not args.followers_tw and not args.followings_tw:
        results.extend(twitter.getUserTweetsWithEmails(
            args.target_tw,
            args.limit,
            args.year,
            args.since,
            args.until,
            args.profile_full,
            args.all_tw))

    if args.target_tw and args.followers_tw or args.followings_tw:
        users = []
        if args.followers_tw:        
            users = twitter.getFollowers(args.target_tw,args.limit)

        if args.followings_tw:
            users.extend(twitter.getFollowings(args.target_tw,args.limit))

        results.extend(twitter.getTweetEmailsFromListOfUsers(
            list(set(users)),
            args.limit,
            args.year,
            args.since,
            args.until,
            args.profile_full,
            args.all_tw))


    if args.hashtag_tw:
        results.extend(twitter.getTweetEmailsFromHashtag(
            args.hashtag_tw,
            args.limit,
            args.year,
            args.since,
            args.until))

    return results

def ghuntParameters(args,ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID,results):
    print(colors.good + " Using GHunt!\n" + colors.end)
    ghunt.checkAndGen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID)

    if args.email_gh:
        ghunt.emailHunt(args.email_gh)
    if results != []:
        ghunt.emailsListHunt(results)
    else:
        print(colors.bad + " No emails for Ghunt" + colors.end)

def dehashedParameters(args,dehashed_email,dehashed_apikey,results,out_dir):
    print(colors.good + " Using Dehashed!\n" + colors.end)

    dehashed_results = []

    if results != []:
        dehashed_results = DehashedAPI.dehashedRequest(dehashed_email,dehashed_apikey,results)
    else:
        print(colors.bad + " No emails for Ghunt" + colors.end)

    if args.email_dh:
        dehashed_results.append(DehashedAPI.dehashedSearch(dehashed_email,dehashed_apikey,email=args.email_dh))

    output.saveResultsDehashed(out_dir,dehashed_results)

def run(args):

    results = []
    creds = ''
    session = 'session_' + datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
    out_dir = 'output/' + session
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if args.credentials and os.path.isfile(args.credentials) and os.access(args.credentials, os.R_OK):
        creds = readCredentials(args.credentials)
    else:
        print(colors.bad + " The file can't be accessed" + colors.end)
        sys.exit()

    if args.pwndb:
        status = os.system('service tor status > /dev/null')
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
        results.extend(linkedinParameters(args,in_email,in_password,out_dir))
    
    if args.twitter:
        results.extend(twitterParameters(args))
    
    if args.ghunt:
        ghunt_SID = creds.get("ghunt").get("SID")
        ghunt_SSID = creds.get("ghunt").get("SSID")
        ghunt_APISID = creds.get("ghunt").get("APISID")
        ghunt_SAPISID = creds.get("ghunt").get("SAPISID")
        ghunt_HSID = creds.get("ghunt").get("HSID")
        ghuntParameters(args,ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID,results)

    if args.dehashed:
        dehashed_email = creds.get("dehashed").get("email")
        dehashed_apikey = creds.get("dehashed").get("apikey")
        dehashedParameters(args,dehashed_email,dehashed_apikey,results,out_dir)

    if results != [] and results != False:
        output.saveEmails(out_dir,results)
        if args.pwndb:
            print(colors.good + " Using PwnDB!\n" + colors.end)
            pwndb_results = PwnDB.findLeak(results,args.tor_proxy)
            output.saveResultsPwnDB(out_dir,pwndb_results)
