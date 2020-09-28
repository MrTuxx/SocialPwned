#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from core.main import run
import core.banner as banner

if __name__ == "__main__":
    banner.banner()
    parser = argparse.ArgumentParser(description="Social Pwned",prog='socialpwned.py',formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40))
    general = parser.add_argument_group("General Arguments","General arguments")
    general.add_argument("--credentials",required=True, action="store", help="Credentials in a JSON file. If you use instagram you must enter the username. If you use LinkedIn you must enter the email.")
    general.add_argument("--pwndb",required=False, action="store_true", help="Searches all the emails published by users in PwnDB and stores the results in the file PwnDBResults.txt")
    general.add_argument("--output",required=False, action="store", help="Save users, users ID and emails found in a file",metavar="FILE")
    general.add_argument("--tor-proxy",default='127.0.0.1:9050', type=str, help="Set Tor proxy (default: 127.0.0.1:9050)",metavar="PROXY")
    instagram = parser.add_argument_group("Instagram Arguments","Specific arguments for Instagram")
    instagram.add_argument("--instagram",required=False, action="store_true", help="You must use this flag if you want to use the Instagram functions")
    instagram.add_argument("--info",required=False, action="store", help="Get information about locations and their IDs.",metavar="QUERY")
    instagram.add_argument("--location",required=False, action="store", help="Get users with public email from a location ID.",metavar="LOCATION_ID")
    instagram.add_argument("--hashtag-ig",required=False, action="store", help="Get users with public email from a hashtag.",metavar="QUERY")
    instagram.add_argument("--target-ig",required=False, action="store", help="Get email, user ID, followers and followings of a specific username.",metavar="USER_ID")
    instagram.add_argument("--search-users-ig",required=False, action="store", help="Search any user in Instagram",metavar="QUERY")
    instagram.add_argument("--my-followers",required=False, action="store_true", help="Get users with public email from your followers")
    instagram.add_argument("--my-followings",required=False, action="store_true", help="Get users with public email from your followings")
    instagram.add_argument("--followers-ig",required=False, action="store_true", help="Get users with public emails from the followers of a target")
    instagram.add_argument("--followings-ig",required=False, action="store_true", help="Get users with public emails from the followings of a target")
    linkedin = parser.add_argument_group("Linkedin Arguments","Specific arguments for Linkedin")
    linkedin.add_argument("--linkedin",required=False, action="store_true", help="You must use this flag if you want to use the LikedIn functions")
    linkedin.add_argument("--company",required=False, action="store", help="Get information about a specific company from company ID",metavar="COMPANY_ID")
    linkedin.add_argument("--search-companies",required=False, action="store", help="Search any company.\nYou can also search for a specific company by entering the exact name",metavar="QUERY")
    linkedin.add_argument("--employees",required=False, action="store_true",help="Get the employees of a company and contact information. If you combine it with the flag --search-companies you get the current and past employees and if you combine it with the flag --company you get only the current employees")
    linkedin.add_argument("--my-contacts",required=False, action="store_true",help="Display my contacts and their contact information")
    linkedin.add_argument("--user-contacts",required=False, action="store",help="Display contacts from a specific user ID and their contact information",metavar="USER_ID")
    linkedin.add_argument("--search-users-in",required=False, action="store",help="Search any user in Linkedin",metavar="QUERY")
    linkedin.add_argument("--target-in",required=False, action="store",help="Get a user's contact information",metavar="USERNAME")
    linkedin.add_argument("--add-contacts",required=False, action="store_true",help="Send contact request for all users")
    linkedin.add_argument("--add-a-contact",required=False, action="store",help="Send contact request for a single user with his user ID",metavar="USER_ID")
    twitter = parser.add_argument_group("Twitter Arguments","Specific arguments for Twitter")
    twitter.add_argument("--twitter",required=False, action="store_true", help="You must use this flag if you want to use the Twitter functions")
    twitter.add_argument("--limit",required=False, action="store", default='100', type=int, help="Number of Tweets to pull (Increments of 20).",metavar="LIMIT")
    twitter.add_argument("--year",required=False, action="store", default=None, type=int, help="Filter Tweets before specified year.",metavar="YEAR")
    twitter.add_argument("--since",required=False, action="store", default=None, type=str, help="Filter Tweets sent since date (Example: 2017-12-27 20:30:15 or 2017-12-27).",metavar="DATE")       
    twitter.add_argument("--until",required=False, action="store", default=None, type=str, help="Filter Tweets sent until date (Example: 2017-12-27 20:30:15 or 2017-12-27).",metavar="DATE")   
    twitter.add_argument("--profile-full",required=False, action="store_true", help="Slow, but effective method of collecting a user's Tweets and RT.")
    twitter.add_argument("--all-tw",required=False, action="store_true", help="Search all Tweets associated with a user.")
    twitter.add_argument("--target-tw",required=False, action="store",help="User's Tweets you want to scrape",metavar="USERNAME")
    twitter.add_argument("--hashtag-tw",required=False, action="store",help="Get tweets containing emails from a hashtag",metavar="USERNAME")
    twitter.add_argument("--followers-tw",required=False, action="store_true", help="Scrape a person's followers.")
    twitter.add_argument("--followings-tw",required=False, action="store_true", help="Scrape a person's follows.")
    args = parser.parse_args()

    run(args)

    