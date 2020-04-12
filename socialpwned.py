#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from core.main import run


if __name__ == "__main__":

    footed_description = """
    Usage examples:\n
        \n
        + Getting information about locations:\n
        \tpython3 %(name)s --user user --password password --info Madrid\n
        + Getting
        +
        +
        +  
        +
        +

    """%dict(name="socialpwned.py")

    parser = argparse.ArgumentParser(description="Social Pwned",prog='socialpwned.py',epilog=footed_description,formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40))
    general = parser.add_argument_group("General Arguments","General arguments")
    general.add_argument("--user", required=True, action="store", help="If you use instagram you must enter the username. If you use LinkedIn you must enter the email.")
    general.add_argument("--password", required=True, action="store", help="Password")
    general.add_argument("--pwndb", required=False, action="store_true", help="Searches all the emails published by users in PwnDB and stores the results in the file PwnDBResults.txt")
    general.add_argument("--delay-pwndb", required=False, action="store", type=float, default="0.5", help="Set delay (in seconds) to PwnDB requests")
    general.add_argument("--output", required=False, action="store", help="Save users, users ID and emails found in a file")
    general.add_argument("--tor-proxy", default='127.0.0.1:9050', type=str, help="Set Tor proxy (default: 127.0.0.1:9050)")
    ig = parser.add_argument_group("Instagram Arguments","Specific arguments for Instagram")
    ig.add_argument("--instagram", required=False, action="store_true", help="You must use this flag if you want to use the Instagram functions")
    ig.add_argument("--info", required=False, action="store", help="Get information about locations and their IDs.")
    ig.add_argument("--location", required=False, action="store", help="Get users with public email from a location ID.")
    ig.add_argument("--hashtag", required=False, action="store", help="Get users with public email from a hashtag.")
    ig.add_argument("--target", required=False, action="store", help="Get email, user ID, followers and followings of a specific username.")
    ig.add_argument("--search-user", required=False, action="store", help="Search any user")
    ig.add_argument("--my-followers", required=False, action="store_true", help="Get users with public email from your followers")
    ig.add_argument("--my-followings", required=False, action="store_true", help="Get users with public email from your followings")
    ig.add_argument("--followers", required=False, action="store_true", help="Get users with public emails from the followers of a target")
    ig.add_argument("--followings", required=False, action="store_true", help="Get users with public emails from the followings of a target")
    ig.add_argument("--delay-ig", required=False, action="store", type=float, default="0.5", help="Set delay (in seconds) to Instagram API requests")
    linkedin = parser.add_argument_group("Linkedin Arguments","Specific arguments for Linkedin")
    linkedin.add_argument("--linkedin", required=False, action="store_true", help="LikedIn")
    linkedin.add_argument("--company", required=False, action="store", help="Get information about a specific company from company ID")
    linkedin.add_argument("--search-companies", required=False, action="store", help="Search any company.\nYou can also search for a specific company by entering the exact name")
    linkedin.add_argument("--employees",required=False,action="store_true",help="Get the employees of a company and contact information. If you combine it with the flag --search-companies you get the current and past employees and if you combine it with the flag --company you get only the current employees")
    linkedin.add_argument("--my-contacts",required=False,action="store_true",help="Display my contacts and their contact information")
    linkedin.add_argument("--user-contacts",required=False,action="store",help="Display contacts from a specific user ID and their contact information")
    linkedin.add_argument("--search-users",required=False,action="store",help="Search any user")
    linkedin.add_argument("--add-contacts",required=False,action="store_true",help="Send contact request for all users")
    linkedin.add_argument("--add-a-contact",required=False,action="store",help="Send contact request for a single user with his userID")
    
    args = parser.parse_args()

    run(args)

    