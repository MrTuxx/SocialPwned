#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from core.main import run


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='socialpwned.py')
    parser.add_argument("--user", required=True, action="store", help="Username")
    parser.add_argument("--password", required=True, action="store", help="Password")
    parser.add_argument("--info", required=False, action="store", help="Get information about locations and their IDs.")
    parser.add_argument("--location", required=False, action="store", help="Get users with public email from a location ID.")
    parser.add_argument("--hashtag", required=False, action="store", help="Get users with public email from a hashtag.")
    parser.add_argument("--target", required=False, action="store", help="Get email, user ID, followers and followings of a specific username.")
    parser.add_argument("--search-user", required=False, action="store", help="Search any user")
    parser.add_argument("--my-followers", required=False, action="store_true", help="Get users with public email from your followers")
    parser.add_argument("--my-followings", required=False, action="store_true", help="Get users with public email from your followings")
    parser.add_argument("--followers", required=False, action="store_true", help="Get users with public emails from the followers of a target")
    parser.add_argument("--followings", required=False, action="store_true", help="Get users with public emails from the followings of a target")
    parser.add_argument("--pwndb", required=False, action="store_true", help="Searches all the emails published by users in PwnDB and stores the results in the file PwnDBResults.txt")
    parser.add_argument("--output", required=False, action="store", help="Save users, users ID and emails found in a file")
    parser.add_argument("--proxy", default='127.0.0.1:9050', type=str, help="Set Tor proxy (default: 127.0.0.1:9050)")
    args = parser.parse_args()

    run(args)

    